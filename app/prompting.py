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
