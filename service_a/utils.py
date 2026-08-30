import os
import time
import httpx

from service_a.config import LOG_FILE


def log_event(msg):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, "a") as f:
        f.write(f"{get_timestamp()} | {msg}\n")


def get_timestamp():
    return time.strftime(
        "%Y-%m-%d %H:%M:%S",
        time.localtime()
    )

# Táctica: Re-intentos
def retry_request(url, retries=3):

    for attempt in range(retries):

        try:
            response = httpx.get(url, timeout=0.8)
            response.raise_for_status()

            log_event(f"Request successful: {url}")

            return response.json()

        except Exception as e:

            log_event(
                f"Retry {attempt + 1} failed for {url}: {e}"
            )

            if attempt < retries - 1:
                time.sleep(0.3)

    raise Exception(f"All retries failed for {url}")


# Táctica: Replicación
def request_with_replication(urls):

    for url in urls:

        try:
            response = httpx.get(url, timeout=0.8)
            response.raise_for_status()

            log_event(f"Instance successful: {url}")

            return response.json()

        except Exception as e:

            log_event(
                f"Instance failed: {url}: {e}"
            )

    raise Exception("All replicated instances failed")
