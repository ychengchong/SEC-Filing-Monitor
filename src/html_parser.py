import warnings

from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning


warnings.filterwarnings(
    "ignore",
    category=XMLParsedAsHTMLWarning
)


def html_to_text(html):
    soup = BeautifulSoup(html, "lxml")

    # Remove code, styling and hidden inline-XBRL information
    unwanted_tags = [
        "script",
        "style",
        "noscript",
        "ix:header",
        "ix:hidden",
        "ix:resources",
        "xbrli:context",
        "xbrli:unit"
    ]

    for tag_name in unwanted_tags:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Process from child to parent to prevent deleted-tag errors
    hidden_tags = list(
        soup.find_all(attrs={"hidden": True})
    )

    for tag in reversed(hidden_tags):
        if tag.parent is not None:
            tag.decompose()

    # Find elements hidden using CSS
    hidden_style_tags = []

    for tag in soup.find_all(style=True):
        # Skip tags that were already deleted
        if tag.attrs is None:
            continue

        style = str(
            tag.get("style", "")
        ).replace(" ", "").lower()

        if "display:none" in style:
            hidden_style_tags.append(tag)

    # Delete children before their parents
    for tag in reversed(hidden_style_tags):
        if tag.parent is not None:
            tag.decompose()

    text = soup.get_text(separator="\n")

    clean_lines = []

    for line in text.splitlines():
        cleaned_line = line.strip()

        if cleaned_line:
            clean_lines.append(cleaned_line)

    # Remove XBRL information before the SEC cover page
    for index, line in enumerate(clean_lines):
        if line.upper() != "UNITED STATES":
            continue

        nearby_lines = clean_lines[
            index + 1:index + 4
        ]

        if any(
            "SECURITIES AND EXCHANGE COMMISSION"
            in nearby_line.upper()
            for nearby_line in nearby_lines
        ):
            clean_lines = clean_lines[index:]
            break

    return "\n".join(clean_lines)