EMOJI_MAP: dict[str, str] = {
    # Earnings
    "basic": "💼",
    "basic salary": "💼",
    "hra": "🏠",
    "house rent allowance": "🏠",
    "da": "📈",
    "dearness allowance": "📈",
    "special allowance": "⭐",
    "lta": "✈️",
    "leave travel allowance": "✈️",
    "medical allowance": "🏥",
    "conveyance": "🚗",
    "conveyance allowance": "🚗",
    "bonus": "🎁",
    "incentive": "🏆",
    "overtime": "⏰",
    "gross": "💰",
    "gross earnings": "💰",
    "gross salary": "💰",
    # Deductions
    "pf": "🏦",
    "provident fund": "🏦",
    "epf": "🏦",
    "esi": "🏥",
    "employee state insurance": "🏥",
    "pt": "🏛️",
    "professional tax": "🏛️",
    "tds": "📋",
    "tax deducted at source": "📋",
    "income tax": "📋",
    "advance": "💳",
    "loan": "💳",
    "total deductions": "➖",
    "net pay": "✅",
    "net salary": "✅",
    "take-home": "✅",
    "take home": "✅",
}

_VIRAL_FOOTER = "\n\n---\n💡 *Found this helpful? Forward to a colleague* 👇"


def format_response(raw: str, language: str) -> str:
    """Prefix known salary component names with emojis and append viral footer.

    Works on the raw LLM text — looks for known keywords at the start of a line
    or after a bullet/dash and prepends the matching emoji.
    """
    lines = raw.splitlines()
    out: list[str] = []

    for line in lines:
        stripped = line.lstrip("-•* \t")
        lower = stripped.lower()

        matched_emoji = ""
        for keyword, emoji in EMOJI_MAP.items():
            # Match keyword at the very start of the meaningful content
            if lower.startswith(keyword):
                matched_emoji = emoji
                break

        if matched_emoji:
            leading = line[: len(line) - len(line.lstrip("-•* \t"))]
            out.append(f"{leading}{matched_emoji} {stripped}")
        else:
            out.append(line)

    return "\n".join(out) + _VIRAL_FOOTER
