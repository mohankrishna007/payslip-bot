"""Format a parsed payslip-analysis dict into a friendly, readable text message.

Supports WhatsApp markdown (*bold*, _italic_) and uses visual separators
so the output is readable both in WhatsApp and in the in-app chat UI.
"""

_SEP = "─────────────────────"


def _amt(value) -> str:
    """Safely format a numeric amount as ₹X,XXX.XX."""
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return f"₹{value}"


def _component_block(c: dict, is_deduction: bool = False) -> list[str]:
    """Return lines for a single earnings or deduction component."""
    block: list[str] = []

    statutory_tag = " 🏛️" if is_deduction and c.get("statutory") else ""
    block.append(f"*{c['label']}*{statutory_tag} — {_amt(c.get('amount', 0))}")

    if c.get("what"):
        block.append(c["what"])
    if c.get("flag"):
        block.append(f"⚠️ _{c['flag']}_")
    if c.get("tip"):
        block.append(f"💡 _{c['tip']}_")

    return block


def format_analysis(data: dict) -> str:
    lines: list[str] = []

    month_year = data.get("month_year", "")
    header = f"🎉 *{month_year} Payslip — decoded just for you!*" if month_year else "🎉 *Your Payslip — decoded!*"
    lines += [header, ""]

    # ── Earnings ─────────────────────────────────────────────────────────────
    earnings = data.get("earnings") or []
    if earnings:
        lines += ["💰 *What you earned*", _SEP, ""]
        for e in earnings:
            lines += _component_block(e, is_deduction=False)
            lines.append("")

    # ── Deductions ────────────────────────────────────────────────────────────
    deductions = data.get("deductions") or []
    if deductions:
        lines += ["➖ *What got deducted*", _SEP, ""]
        for d in deductions:
            lines += _component_block(d, is_deduction=True)
            lines.append("")

    # ── Summary numbers ───────────────────────────────────────────────────────
    gross = data.get("gross", 0)
    total_ded = data.get("total_deductions", 0)
    net = data.get("net_pay", 0)

    lines += [
        "📊 *The big picture*", _SEP, "",
        f"Gross earned      {_amt(gross)}",
        f"Total deducted    {_amt(total_ded)}",
        "",
        f"✅ *In your account: {_amt(net)}*",
        "",
    ]

    # ── Summary ───────────────────────────────────────────────────────────────
    summary = (data.get("summary") or "").strip()
    if summary:
        lines += ["📝 " + summary, ""]

    # ── Follow-up question ────────────────────────────────────────────────────
    followup = (data.get("followup") or "").strip()
    if followup:
        lines.append(f"💬 {followup}")

    return "\n".join(lines)
