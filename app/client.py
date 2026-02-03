import os
import time
import random
import logging
import requests

TIMEOUT_SECONDS = 30
MAX_RETRIES = 3

logger = logging.getLogger(__name__)

def call_openai_api(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing API key. Please set OPENAI_API_KEY in your environment.")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            start = time.time()
            response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
            elapsed = round(time.time() - start, 2)

            logger.info(f"OpenAI API status={response.status_code} time={elapsed}s attempt={attempt}")

            # Success
            if response.status_code == 200:
                result = response.json()
                if "choices" not in result or not result["choices"]:
                    raise ValueError("Unexpected API response: no choices")
                return result["choices"][0]["message"]["content"]

            # Retryable errors (rate limit + server errors)
            if response.status_code in (429, 500, 502, 503, 504):
                last_error = f"HTTP {response.status_code}: {response.text}"
                sleep_s = (2 ** (attempt - 1)) + random.random()
                time.sleep(sleep_s)
                continue

            # Non-retryable errors
            raise requests.RequestException(f"HTTP {response.status_code}: {response.text}")

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            last_error = str(e)
            sleep_s = (2 ** (attempt - 1)) + random.random()
            time.sleep(sleep_s)
            continue

    raise RuntimeError(f"OpenAI API failed after {MAX_RETRIES} retries. Last error: {last_error}")
