from app.services.deduction_checker import check


def test_pf_correct():
    results = check({"basic": 25000, "pf": 3000, "gross": 40000})
    pf = next(r for r in results if r["field"] == "PF")
    assert pf["status"] == "ok"


def test_pf_wrong_amount_flagged():
    # Expected ₹3,000 (12% of ₹25,000), but actual is ₹1,000
    results = check({"basic": 25000, "pf": 1000, "gross": 40000})
    pf = next(r for r in results if r["field"] == "PF")
    assert pf["status"] == "flag"


def test_pf_missing_when_mandatory():
    # Basic > ₹15,000 and no PF — should flag
    results = check({"basic": 20000, "gross": 30000})
    pf = next((r for r in results if r["field"] == "PF"), None)
    assert pf is not None
    assert pf["status"] == "flag"


def test_esi_correct_when_gross_below_threshold():
    # gross = ₹18,000 → ESI = 0.75% = ₹135
    results = check({"basic": 12000, "gross": 18000, "esi": 135})
    esi = next(r for r in results if r["field"] == "ESI")
    assert esi["status"] == "ok"


def test_esi_flagged_when_gross_above_threshold():
    # gross >= ₹21,000 — ESI should NOT be deducted
    results = check({"basic": 20000, "gross": 25000, "esi": 188})
    esi = next(r for r in results if r["field"] == "ESI")
    assert esi["status"] == "flag"


def test_pt_correct_maharashtra():
    results = check({"basic": 15000, "gross": 20000, "pt": 200, "state": "maharashtra"})
    pt = next(r for r in results if r["field"] == "PT")
    assert pt["status"] == "ok"


def test_pt_wrong_amount_flagged():
    results = check({"basic": 15000, "gross": 20000, "pt": 150, "state": "maharashtra"})
    pt = next(r for r in results if r["field"] == "PT")
    assert pt["status"] == "flag"


def test_no_results_for_empty_components():
    assert check({}) == []


def test_string_values_parsed_correctly():
    # Values may come as strings with commas from regex extraction
    results = check({"basic": "25,000", "pf": "3,000", "gross": "40,000"})
    pf = next(r for r in results if r["field"] == "PF")
    assert pf["status"] == "ok"
