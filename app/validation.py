import re
from typing import Tuple, Dict
MIN_LENGTH = 20
MAX_LENGTH = 1500
REPEAT_RATIO_THRESHOLD = 0.5


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

    return True, text 