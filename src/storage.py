import json
import os


def save_filings_to_json(filings, file_path="data/filings.json"):
    os.makedirs("data", exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(
            filings,
            json_file,
            indent=4,
            ensure_ascii=False
        )