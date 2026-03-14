import re


class PIIScrubber:
    """Removes PII (PAN numbers and bank account numbers) from text.

    Both patterns are compiled once at class definition time.
    """

    # PAN: 5 uppercase letters, 4 digits, 1 uppercase letter (e.g. ABCDE1234F)
    _PAN_RE = re.compile(r'[A-Z]{5}[0-9]{4}[A-Z]')

    # Bank account numbers: 9–18 consecutive digits.
    # Negative lookbehind/ahead on ₹ and , prevents matching rupee amounts.
    _ACCOUNT_RE = re.compile(r'(?<![₹,\d])\b\d{9,18}\b(?![,\d])')

    def scrub(self, text: str) -> str:
        """Replace PAN and bank account numbers with [REDACTED].

        Safe to call on clean text — short numbers (e.g. rupee amounts)
        and comma-formatted figures are not matched.
        """
        text = self._PAN_RE.sub("[REDACTED]", text)
        text = self._ACCOUNT_RE.sub("[REDACTED]", text)
        return text


# Module-level singleton and backward-compatible alias.
_scrubber = PIIScrubber()
scrub = _scrubber.scrub
