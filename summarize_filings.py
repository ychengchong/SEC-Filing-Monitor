import json
from pathlib import Path

from src.summarizer import create_summary


def main():
    processed_file = Path("data/processed_filings.json")
    summaries_file = Path("data/summaries.json")

    if not processed_file.exists():
        print("data/processed_filings.json was not found.")
        print("Run process_filings.py first.")
        return

    with processed_file.open("r", encoding="utf-8") as json_file:
        filings = json.load(json_file)

    summaries = []

    for number, filing in enumerate(filings, start=1):
        company = filing["company"]
        form = filing["form"]

        print(
            f"Summarising {number}/{len(filings)}: "
            f"{company} {form}"
        )

        if filing.get("processing_status") != "successful":
            print("Skipped because HTML processing failed.")
            continue

        text_path = Path(filing["text_path"])

        if not text_path.exists():
            print(f"Skipped because {text_path} was not found.")
            continue

        clean_text = text_path.read_text(encoding="utf-8")

        summary_result = create_summary(
            clean_text,
            form=filing["form"]
        )

        summary_record = {
            "company": filing["company"],
            "ticker": filing["ticker"],
            "cik": filing["cik"],
            "form": filing["form"],
            "filing_date": filing["filing_date"],
            "accession_number": filing["accession_number"],
            "filing_url": filing["filing_url"],
            "event_type": summary_result["event_type"],
            "summary": summary_result["summary"],
            "source_word_count": summary_result["source_word_count"],
            "summary_method": summary_result["summary_method"]
        }

        summaries.append(summary_record)

    with summaries_file.open("w", encoding="utf-8") as json_file:
        json.dump(
            summaries,
            json_file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)
    print(f"Summaries created: {len(summaries)}")
    print(f"Saved to: {summaries_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()