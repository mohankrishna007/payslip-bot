"""Domain models — validated representations of a parsed payslip."""

from pydantic import BaseModel, ConfigDict


class PayslipComponent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    label: str
    amount: float = 0.0
    what: str = ""
    why: str | None = None
    flag: str | None = None
    tip: str | None = None


class PayslipDeduction(PayslipComponent):
    statutory: bool = False


class PayslipData(BaseModel):
    model_config = ConfigDict(extra="ignore")
    month_year: str = ""
    earnings: list[PayslipComponent] = []
    deductions: list[PayslipDeduction] = []
    gross: float = 0.0
    total_deductions: float = 0.0
    net_pay: float = 0.0
    summary: str = ""
    followup: str = ""
