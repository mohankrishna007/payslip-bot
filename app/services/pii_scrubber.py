import re

# PAN: 5 uppercase letters, 4 digits, 1 uppercase letter (e.g. ABCDE1234F)
_PAN_RE = re.compile(r'[A-Z]{5}[0-9]{4}[A-Z]')

# Bank account numbers: 9–18 consecutive digits
# The negative lookbehind/ahead on ₹ and , prevents matching rupee amounts
_ACCOUNT_RE = re.compile(r'(?<![₹,\d])\b\d{9,18}\b(?![,\d])')


def scrub(text: str) -> str:
    """Remove PAN numbers and bank account numbers from text.

    Replaces matches with [REDACTED]. Safe to call on clean text —
    short numbers (e.g. rupee amounts) and comma-formatted figures
    are not matched.
    """
    text = _PAN_RE.sub("[REDACTED]", text)
    text = _ACCOUNT_RE.sub("[REDACTED]", text)
    return text
