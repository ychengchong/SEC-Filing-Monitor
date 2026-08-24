import time

import requests


def download_filing_html(
    filing_url,
    headers,
    maximum_attempts=3
):
    for attempt in range(1, maximum_attempts + 1):
        try:
            response = requests.get(
                filing_url,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            return response.text

        except (
            requests.ConnectionError,
            requests.Timeout
        ) as error:

            if attempt == maximum_attempts:
                raise

            waiting_time = 2 ** (attempt - 1)

            print(
                f"Connection failed. "
                f"Retrying in {waiting_time} seconds..."
            )

            time.sleep(waiting_time)