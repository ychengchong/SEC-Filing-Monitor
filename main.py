import time
import requests

from config import (
    WATCHLIST,
    SEC_HEADERS,
    WANTED_FORMS,
    MAX_FILINGS_PER_COMPANY
)

from src.sec_client import get_recent_filings
from src.storage import save_filings_to_json

def main():

    print("=" * 60)
    print("MARKET PULSE — SEC FILING MONITOR")
    print("=" * 60)

    all_filings = []

    for company_name, company_details in WATCHLIST.items():

        ticker = company_details["ticker"]

        print(f"\nChecking {company_name} ({ticker})...")

        try:
            filings = get_recent_filings(
                company_name=company_name,
                company_details=company_details,
                headers=SEC_HEADERS,
                wanted_forms=WANTED_FORMS,
                maximum_filings=MAX_FILINGS_PER_COMPANY
            )

        except requests.RequestException as error:
            print(f"Unable to retrieve filings: {error}")
            continue

        if not filings:
            print("No relevant filings found.")
            continue

        all_filings.extend(filings)

        for filing in filings:
            print(f"\nForm: {filing['form']}")
            print(f"Date: {filing['filing_date']}")
            print(f"Link: {filing['filing_url']}")
            print("-" * 60)

        # Pause briefly before checking the next company
        time.sleep(0.2)

    print(f"\nTotal filings collected: {len(all_filings)}")

    save_filings_to_json(all_filings)
    print("Filings saved to data/filings.json")

if __name__ == "__main__":
    main()