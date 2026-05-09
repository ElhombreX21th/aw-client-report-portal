from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ClientReportInput:
    """Input values collected from the quarterly report form."""

    client_name: str = "John & Jane Doe"
    quarter: str = "Q1 2026"
    retirement_husband: Decimal = Decimal("450000")
    retirement_wife: Decimal = Decimal("320000")
    non_retirement: Decimal = Decimal("180000")
    trust: Decimal = Decimal("250000")
    house_value: Decimal = Decimal("850000")
    liabilities: Decimal = Decimal("120000")
    salary_income: Decimal = Decimal("12000")
    social_security: Decimal = Decimal("3500")
    pension_income: Decimal = Decimal("3000")
    other_inflow: Decimal = Decimal("0")
    mortgage: Decimal = Decimal("3500")
    taxes: Decimal = Decimal("1400")
    living_expenses: Decimal = Decimal("4200")
    insurance: Decimal = Decimal("900")
    other_outflow: Decimal = Decimal("0")

    def to_query_params(self) -> dict[str, str]:
        return {key: str(value) for key, value in asdict(self).items()}
