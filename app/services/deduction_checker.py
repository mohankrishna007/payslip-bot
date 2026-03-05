import re


# PT rules: state → (monthly_amount, min_salary_threshold)
PT_RULES: dict[str, tuple[float, float]] = {
    "maharashtra": (200.0, 10_000.0),
}

_TOLERANCE = 0.05  # ±5%


def _extract_number(value) -> float | None:
    """Coerce a value to float, stripping currency symbols and commas."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = re.sub(r"[₹,\s]", "", value)
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def check(components: dict) -> list[dict]:
    """Check statutory deduction correctness.

    Args:
        components: dict with keys like 'basic', 'gross', 'pf', 'esi', 'pt', 'state'.
                    Keys are case-insensitive. Values may be numbers or strings.

    Returns:
        List of dicts: {field, expected, actual, status: "ok" | "flag"}
    """
    # Normalise keys
    c = {k.lower().strip(): v for k, v in components.items()}
    results: list[dict] = []

    basic = _extract_number(c.get("basic") or c.get("basic salary"))
    gross = _extract_number(c.get("gross") or c.get("gross salary") or c.get("gross earnings"))
    pf_actual = _extract_number(c.get("pf") or c.get("provident fund") or c.get("epf"))
    esi_actual = _extract_number(c.get("esi") or c.get("employee state insurance"))
    pt_actual = _extract_number(c.get("pt") or c.get("professional tax"))
    state = str(c.get("state", "maharashtra")).lower().strip()

    # --- PF check ---
    if basic is not None and pf_actual is not None:
        pf_expected = round(basic * 0.12, 2)
        tolerance = pf_expected * _TOLERANCE
        status = "ok" if abs(pf_actual - pf_expected) <= tolerance else "flag"
        results.append({
            "field": "PF",
            "expected": pf_expected,
            "actual": pf_actual,
            "status": status,
        })
    elif basic is not None and basic > 15_000 and pf_actual is None:
        # Mandatory if basic > ₹15,000 but not found
        results.append({
            "field": "PF",
            "expected": round(basic * 0.12, 2),
            "actual": None,
            "status": "flag",
        })

    # --- ESI check ---
    if gross is not None:
        if gross < 21_000:
            if esi_actual is not None:
                esi_expected = round(gross * 0.0075, 2)
                tolerance = esi_expected * _TOLERANCE
                status = "ok" if abs(esi_actual - esi_expected) <= tolerance else "flag"
                results.append({
                    "field": "ESI",
                    "expected": esi_expected,
                    "actual": esi_actual,
                    "status": status,
                })
        else:
            # ESI should NOT be deducted when gross >= ₹21,000
            if esi_actual is not None and esi_actual > 0:
                results.append({
                    "field": "ESI",
                    "expected": 0,
                    "actual": esi_actual,
                    "status": "flag",
                })

    # --- PT check ---
    if pt_actual is not None and state in PT_RULES:
        pt_expected, min_salary = PT_RULES[state]
        ref_salary = gross if gross is not None else basic
        if ref_salary is not None and ref_salary > min_salary:
            status = "ok" if abs(pt_actual - pt_expected) <= 1 else "flag"
            results.append({
                "field": "PT",
                "expected": pt_expected,
                "actual": pt_actual,
                "status": status,
            })

    return results
