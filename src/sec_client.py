import requests


def build_filing_url(cik, accession_number, primary_document):
    """
    Create the URL for an individual SEC filing.
    """

    # Remove the leading zeros from the CIK
    cik_without_leading_zeros = str(int(cik))

    # Remove dashes from the accession number
    accession_without_dashes = accession_number.replace("-", "")

    filing_url = (
        "https://www.sec.gov/Archives/edgar/data/"
        f"{cik_without_leading_zeros}/"
        f"{accession_without_dashes}/"
        f"{primary_document}"
    )

    return filing_url


def get_recent_filings(
    company_name,
    company_details,
    headers,
    wanted_forms,
    maximum_filings=5
):
    """
    Retrieve the latest important SEC filings for one company.
    """

    ticker = company_details["ticker"]
    cik = company_details["cik"]

    api_url = f"https://data.sec.gov/submissions/CIK{cik}.json"

    # Ask the SEC API for the company's data
    response = requests.get(
        api_url,
        headers=headers,
        timeout=30
    )

    # Raise an error if the request was unsuccessful
    response.raise_for_status()

    # Convert the JSON response into a Python dictionary
    data = response.json()

    recent = data["filings"]["recent"]

    forms = recent["form"]
    filing_dates = recent["filingDate"]
    accession_numbers = recent["accessionNumber"]
    primary_documents = recent["primaryDocument"]

    collected_filings = []

    for form, filing_date, accession, document in zip(
        forms,
        filing_dates,
        accession_numbers,
        primary_documents
    ):

        if form not in wanted_forms:
            continue

        filing_url = build_filing_url(
            cik=cik,
            accession_number=accession,
            primary_document=document
        )

        filing = {
            "company": company_name,
            "ticker": ticker,
            "cik": cik,
            "form": form,
            "filing_date": filing_date,
            "accession_number": accession,
            "document": document,
            "filing_url": filing_url
        }

        collected_filings.append(filing)

        if len(collected_filings) == maximum_filings:
            break

    return collected_filings