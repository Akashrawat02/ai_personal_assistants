from __future__ import annotations

BLOCK_PATTERNS = [
    "phishing", "steal password", "browser passwords", "hack my neighbor",
    "make a bomb", "malware", "keylogger", "threatening my manager",
]

SAFE_RESPONSE = (
    "I can't help with harmful, illegal, or abusive instructions. "
    "I can help with a safe alternative, such as cybersecurity awareness, defensive best practices, "
    "or rewriting the message in a calm and professional tone."
)

def input_guardrail(user_text: str) -> tuple[bool, str | None]:
    text = user_text.lower()
    if any(p in text for p in BLOCK_PATTERNS):
        return False, SAFE_RESPONSE
    return True, None

def system_prompt() -> str:
    return (
        "You are a helpful AI personal assistant. Keep answers concise and practical. "
        "Use conversation history for context. If you are unsure, say so. "
        "Do not invent facts. Avoid stereotypes and discriminatory assumptions. "
        "Refuse requests that are harmful, illegal, unsafe, or violate privacy."
    )
