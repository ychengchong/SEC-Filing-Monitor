# Market Pulse

Market Pulse is an end-to-end SEC filing ingestion and summarisation pipeline built. It collects recent filings for Apple, Microsoft, and Tesla, converts the filing HTML into clean text, creates rule-based filing highlights, and displays the results in a Streamlit dashboard.

## Pipeline

```mermaid
flowchart LR
    A["SEC filings"] --> B["Metadata collection"]
    B --> C["HTML download"]
    C --> D["Text extraction"]
    D --> E["Classification and summary"]
    E --> F["Streamlit dashboard"]
```

| Script | Purpose | Main output |
|---|---|---|
| `main.py` | Collects recent filing metadata for the configured watchlist. | `data/filings.json` |
| `process_filings.py` | Downloads filing HTML and converts it into clean text. | `data/raw_html/` and `data/clean_text/` |
| `summarize_filings.py` | Classifies filings and creates extractive highlights. | `data/summaries.json` |
| `dashboard.py` | Displays and filters the saved summaries. | Local Streamlit dashboard |

The main configuration is stored in `config.py`, including the company watchlist, SEC request headers, filing forms, and filing limit.

## Environment setup

Python 3.10 or newer is recommended.

## Project structure

```text
Market Pulse/
├── config.py
├── main.py
├── process_filings.py
├── summarize_filings.py
├── dashboard.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── sec_client.py
│   ├── filing_downloader.py
│   ├── html_parser.py
│   └── summarizer.py
├── test/
│   └── test_sec_client.py
├── data/
│   ├── filings.json
│   ├── summaries.json
│   ├── raw_html/
│   └── clean_text/
└── log/
```

### Windows PowerShell

```powershell
cd "C:\path\to\Market Pulse"
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& ".\.venv\Scripts\Activate.ps1"
python -m pip install -r requirements.txt
```

### macOS or Linux

```bash
cd "/path/to/Market Pulse"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Before collecting fresh data, update the `User-Agent` in `config.py` with a genuine contact email, as requested by the SEC:

```python
SEC_HEADERS = {
    "User-Agent": "Market Pulse project your-email@example.com"
}
```

## Run the complete pipeline

Run the following commands from the project directory in this order:

### 1. Run the test

```powershell
python -m unittest discover -s test
```

Expected result:

```text
Ran 1 test in ...
OK
```

### 2. Collect filing metadata

```powershell
python main.py
```

Expected output:

```text
Total filings collected: 15
Filings saved to data/filings.json
```

### 3. Download and clean the filings

```powershell
python process_filings.py
```

This creates the raw HTML files in `data/raw_html/` and readable text files in `data/clean_text/`.

### 4. Create the summaries

```powershell
python summarize_filings.py
```

Expected output:

```text
Summaries created: 15
Saved to: data/summaries.json
```

### 5. Open the dashboard

```powershell
python -m streamlit run dashboard.py
```

Streamlit should open the dashboard automatically. Otherwise, open:

```text
http://localhost:8501
```

Keep the terminal open while using the dashboard. Press `Ctrl + C` to stop it.

## Run only the dashboard

If `data/summaries.json` is already included and no data refresh is required, only activate the environment and run:

```powershell
& ".\.venv\Scripts\Activate.ps1"
python -m streamlit run dashboard.py
```

## Expected project outputs

```text
data/
├── filings.json
├── summaries.json
├── raw_html/
└── clean_text/
```

The dashboard should allow the reviewer to filter records by company and filing form, view the detected event type and filing highlight, and open the corresponding official SEC filing.

## Notes

- Internet access is required when running `main.py` and `process_filings.py` with fresh SEC data.
- The included summariser is deterministic and rule-based; it does not require a generative-AI API key.
- The current proof of concept is optimised for `8-K` and `10-Q` filings.
- Saved JSON, HTML, and text files provide checkpoints between pipeline stages, so the entire pipeline does not need to be rerun just to reopen the dashboard.
