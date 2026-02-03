# =========================
# 0) Imports
# =========================
import os
import re
import logging
from app.validation import validate_user_input
from app.prompting import build_business_prompt
from app.client import call_openai_api
from typing import Tuple, Dict

import requests
import streamlit as st
import time

# =========================
# 1) Logging (simple)
# =========================
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


# =========================
# 2) Load API key
# =========================
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Missing API key. Please set OPENAI_API_KEY in your environment.")
    st.stop()


# =========================
# 3) Validation constants
# =========================
MIN_LENGTH = 20
MAX_LENGTH = 1500  # ✅ You said 500 feels too short; adjust for MVP
TIMEOUT_SECONDS = 30

# Allow basic English characters + spaces + basic punctuation
ALLOWED_PATTERN = re.compile(r'^[A-Za-z0-9\s.,?!\'"\-:$]+$')

COMMON_VERBS = {
    "am", "is", "are", "was", "were",
    "be", "been", "being",
    "do", "does", "did",
    "have", "has", "had",
    "can", "could", "will", "would", "should", "may", "might", "must",
    "make", "made", "get", "got", "go", "went",
    "review", "share", "send", "confirm", "update", "attach", "agree", "discuss"
}

REPEAT_RATIO_THRESHOLD = 0.5


# =========================
# 4) Normalize text (fix “smart punctuation”)
# =========================
def normalize_text(text: str) -> str:
    replacements: Dict[str, str] = {
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "\u00A0": " ",  # non-breaking space
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


# =========================
# 5) Validation layer
# =========================
def validate_user_input(raw_text: str) -> Tuple[bool, str]:
    text = normalize_text(raw_text).strip()

    if not text:
        return False, "Input cannot be empty."

    if len(text) < MIN_LENGTH:
        return False, f"Too short. Please enter at least {MIN_LENGTH} characters."

    if len(text) > MAX_LENGTH:
        return False, f"Too long. Please keep it under {MAX_LENGTH} characters."

    if not ALLOWED_PATTERN.match(text):
        return False, "Only English letters and basic punctuation are allowed. No emojis or special symbols."

    words = re.findall(r"[A-Za-z']+", text.lower())
    if len(words) < 5:
        return False, "Please enter a meaningful sentence (at least 5 words)."

    has_verb = any(w in COMMON_VERBS for w in words)
    if not has_verb:
        return False, "Please include at least one verb (e.g., is/are, will, review, share)."

    counts: Dict[str, int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    max_repeat = max(counts.values())
    repeat_ratio = max_repeat / len(words)
    if repeat_ratio > REPEAT_RATIO_THRESHOLD:
        return False, "Too many repeated words. Please rewrite your sentence."

    return True, text  # ✅ cleaned text returned


# =========================
# 6) Prompt builder
# =========================
def build_business_prompt(user_text: str, mode: str) -> str:
    if mode == "Correct + 3 paragraphs":
        return f"""
You are a professional business English editor and communication consultant.

Task:
1) Correct grammar and wording.
2) Output EXACTLY three short paragraphs (no extra blank lines).
3) Keep the tone polite, confident, and manager-ready.
4) Do NOT add emojis.
5) Do NOT add extra headings.

User text:
{user_text}
""".strip()

    # Example: other mode
    return f"""
You are a professional business English editor.

Task:
- Rewrite the text in a concise, polite, manager-ready style.
- Keep it as ONE paragraph.
- No emojis, no headings.

User text:
{user_text}
""".strip()


# =========================
# 7) API client layer
# =========================
def call_openai_api(prompt: str) -> str:
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


# =========================
# 8) UI layer
# =========================
st.title("Business English Sentence Optimizer")

if "processing" not in st.session_state:
    st.session_state.processing = False

disabled = st.session_state.processing  # ✅ lock UI while processing

mode = st.selectbox(
    "Choose mode:",
    ["Correct + 3 paragraphs", "Rewrite (1 paragraph)"],
    disabled=disabled,
)

user_text_raw = st.text_area(
    f"Enter your English text ({MIN_LENGTH}–{MAX_LENGTH} chars):",
    placeholder="Example: Please review the attached proposal and share your feedback.",
    height=150,
    disabled=disabled,  # ✅ disables editing while processing
)

status = st.empty()

clicked = st.button("Generate", disabled=disabled)

if clicked:
    # If already processing, block repeated clicks
    if st.session_state.processing:
        st.warning("Processing... Please wait.")
    else:
        st.session_state.processing = True  # ✅ lock immediately
        status.info("Processing... please wait.")

        try:
            is_valid, cleaned_or_msg = validate_user_input(user_text_raw)
            if not is_valid:
                st.error(cleaned_or_msg)  # ✅ show error
            else:
                prompt = build_business_prompt(cleaned_or_msg, mode)

                with st.spinner("Generating..."):
                    start = time.time()
                    final_text = call_openai_api(prompt)
                elapsed = round(time.time() - start, 2)
                st.caption(f"time={elapsed}s")
                status.success("Done.")
                st.markdown(final_text)

        except requests.exceptions.Timeout:
            status.error("Request timed out. Try a shorter input or try again.")

        except Exception as e:
            status.error(f"Error: {e}")
            logger.exception("Unexpected error")

        finally:
            st.session_state.processing = False  # ✅ always unlock
            # If you want status to disappear after unlock:
            # status.empty()
