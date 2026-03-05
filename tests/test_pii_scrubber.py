from app.services.pii_scrubber import scrub


def test_pan_is_redacted():
    assert scrub("Employee PAN: ABCDE1234F details") == "Employee PAN: [REDACTED] details"


def test_multiple_pans_redacted():
    text = "PAN1: AAAAA0000A and PAN2: ZZZZZ9999Z"
    result = scrub(text)
    assert "[REDACTED]" in result
    assert "AAAAA0000A" not in result
    assert "ZZZZZ9999Z" not in result


def test_account_number_redacted():
    assert scrub("Account: 123456789012") == "Account: [REDACTED]"


def test_clean_text_passes_through():
    text = "Basic Salary: ₹25,000\nNet Pay: ₹35,000"
    assert scrub(text) == text


def test_no_false_positive_rupee_amounts():
    # Short numbers like ₹200, ₹10000 must NOT be redacted
    text = "PT: ₹200\nTDS: ₹5000\nBonus: ₹8000"
    assert scrub(text) == text


def test_no_false_positive_comma_formatted():
    # ₹35,000 and ₹1,25,000 must not be redacted
    text = "Gross: ₹35,000\nCTC: ₹1,25,000"
    assert scrub(text) == text


def test_pan_boundary_not_matched_partial():
    # 9-char string should not match PAN (5+4+1=10 chars required)
    assert scrub("CODE12345") == "CODE12345"
