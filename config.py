# Companies that Market Pulse will monitor
WATCHLIST = {
    "Apple": {
        "ticker": "AAPL",
        "cik": "0000320193"
    },
    "Microsoft": {
        "ticker": "MSFT",
        "cik": "0000789019"
    },
    "Tesla": {
        "ticker": "TSLA",
        "cik": "0001318605"
    }
}


SEC_HEADERS = {
    "User-Agent": "Tan Yi Cheng project",
    "Accept-Encoding": "gzip, deflate"
}


# Filings we want to collect
WANTED_FORMS = {
    "8-K",
    "10-Q",
    "10-K"
}


# Number of filings to show for each company
MAX_FILINGS_PER_COMPANY = 5
