import os
import re
import logging

TIMEOUT_SECONDS = 30

logger = logging.getLogger(__name__)

def call_openai_api(prompt: str) -> str:
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise RuntimeError("Missing API key. Please set OPENAI_API_KEY in your environment.")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    logger.info("Calling OpenAI API...")
    response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)

    if response.status_code != 200:
        # Return readable error for debugging
        raise requests.RequestException(f"HTTP {response.status_code}: {response.text}")

    result = response.json()

    if "choices" not in result or not result["choices"]:
        raise ValueError(f"Unexpected API response (no choices): {result}")

    return result["choices"][0]["message"]["content"]
