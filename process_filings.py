import json
import time
from pathlib import Path

import requests

from config import SEC_HEADERS
from src.filing_downloader import download_filing_html
from src.html_parser import html_to_text


# Use 3 while testing.
# Use None to process every filing.
PROCESS_LIMIT = None


def main():
    filings_file = Path("data/filings.json")
    raw_html_folder = Path("data/raw_html")
    clean_text_folder = Path("data/clean_text")
    output_file = Path("data/processed_filings.json")

    # Create the output folders if they do not exist
    raw_html_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    clean_text_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # main.py must create this first
    if not filings_file.exists():
        print("data/filings.json was not found.")
        print("Run main.py first.")
        return

    # Load the filing metadata
    with filings_file.open(
        "r",
        encoding="utf-8"
    ) as json_file:
        filings = json.load(json_file)

    # Decide whether to process some or all filings
    if PROCESS_LIMIT is None:
        filings_to_process = filings
    else:
        filings_to_process = filings[:PROCESS_LIMIT]

    print(f"Loaded {len(filings)} filing records.")
    print(f"Processing {len(filings_to_process)} filings.")

    processed_filings = []
    successful = 0
    failed = 0

    for number, filing in enumerate(
        filings_to_process,
        start=1
    ):
        company = filing["company"]
        form = filing["form"]
        accession_number = filing["accession_number"]
        filing_url = filing["filing_url"]

        print(
            f"\nProcessing {number}/"
            f"{len(filings_to_process)}: "
            f"{company} {form}"
        )

        # Create the paths before downloading
        html_path = (
            raw_html_folder /
            f"{accession_number}.html"
        )

        text_path = (
            clean_text_folder /
            f"{accession_number}.txt"
        )

        # Copy the original filing metadata
        processed_record = filing.copy()

        try:
            # Use the saved HTML if it already exists
            if (
                html_path.exists()
                and html_path.stat().st_size > 0
            ):
                print("Using previously downloaded HTML.")

                html = html_path.read_text(
                    encoding="utf-8"
                )

            else:
                print("Downloading filing from the SEC...")

                html = download_filing_html(
                    filing_url=filing_url,
                    headers=SEC_HEADERS
                )

                # Save the raw HTML
                html_path.write_text(
                    html,
                    encoding="utf-8"
                )

                print(f"HTML saved: {html_path}")

            # Convert the HTML into readable text
            clean_text = html_to_text(html)

            if not clean_text.strip():
                raise ValueError(
                    "No readable text was extracted."
                )

            # Save the cleaned text
            text_path.write_text(
                clean_text,
                encoding="utf-8"
            )

            processed_record["html_path"] = (
                html_path.as_posix()
            )

            processed_record["text_path"] = (
                text_path.as_posix()
            )

            processed_record["text_characters"] = (
                len(clean_text)
            )

            processed_record["processing_status"] = (
                "successful"
            )

            processed_record["processing_error"] = None

            print(f"Text saved: {text_path}")

            print(
                f"Characters extracted: "
                f"{len(clean_text):,}"
            )

            successful += 1

        except requests.RequestException as error:
            processed_record["processing_status"] = (
                "failed"
            )

            processed_record["processing_error"] = str(error)
            processed_record["html_path"] = None
            processed_record["text_path"] = None
            processed_record["text_characters"] = 0

            print(f"Download failed: {error}")

            failed += 1

        except OSError as error:
            processed_record["processing_status"] = (
                "failed"
            )

            processed_record["processing_error"] = str(error)
            processed_record["html_path"] = None
            processed_record["text_path"] = None
            processed_record["text_characters"] = 0

            print(f"Unable to read or save file: {error}")

            failed += 1

        except Exception as error:
            processed_record["processing_status"] = (
                "failed"
            )

            processed_record["processing_error"] = str(error)
            processed_record["html_path"] = None
            processed_record["text_path"] = None
            processed_record["text_characters"] = 0

            print(f"Unexpected processing error: {error}")

            failed += 1

        processed_filings.append(processed_record)

        # Pause before moving to the next filing
        time.sleep(0.2)

    # Save information about all successful and failed records
    with output_file.open(
        "w",
        encoding="utf-8"
    ) as json_file:
        json.dump(
            processed_filings,
            json_file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)
    print(f"Successfully processed: {successful}")
    print(f"Failed: {failed}")
    print(f"Results saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()