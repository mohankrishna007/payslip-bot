from app.providers.base import LLMProvider

_MOCK_RESPONSE = """\
💼 Salary Slip Summary

Basic Salary: ₹25,000
HRA (House Rent Allowance): ₹10,000
Special Allowance: ₹5,000
Gross Earnings: ₹40,000

Deductions:
- PF (Provident Fund): ₹3,000 — 12% of Basic. Goes into your retirement savings account.
- ESI (Employee State Insurance): ₹300 — 0.75% of Gross. Covers health insurance benefits.
- Professional Tax: ₹200 — State-mandated tax (Maharashtra).
- TDS (Tax Deducted at Source): ₹1,500 — Income tax deducted monthly based on your annual estimate.

Total Deductions: ₹5,000
Net Take-Home Pay: ₹35,000

✅ All deductions appear statutory and correctly calculated.
"""


class MockProvider(LLMProvider):
    async def analyze_image(self, image_bytes: bytes, prompt: str) -> str:
        return _MOCK_RESPONSE
