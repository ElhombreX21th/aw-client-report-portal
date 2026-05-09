from __future__ import annotations

from decimal import Decimal

from app.models import ClientReportInput


def calculate_total_inflow(data: ClientReportInput) -> Decimal:
    """Return quarterly cash inflows across all configured sources."""

    return data.salary_income + data.social_security + data.pension_income + data.other_inflow


def calculate_total_outflow(data: ClientReportInput) -> Decimal:
    """Return quarterly cash outflows across all configured categories."""

    return data.mortgage + data.taxes + data.living_expenses + data.insurance + data.other_outflow


def calculate_private_reserve(data: ClientReportInput) -> Decimal:
    """Return excess cash available for the private reserve."""

    return calculate_total_inflow(data) - calculate_total_outflow(data)


def calculate_net_worth(data: ClientReportInput) -> Decimal:
    """Return total net worth using the assessment formula."""

    retirement_total = data.retirement_husband + data.retirement_wife
    return retirement_total + data.non_retirement + data.trust + data.house_value - data.liabilities


def calculate_retirement_total(data: ClientReportInput) -> Decimal:
    """Return combined retirement assets."""

    return data.retirement_husband + data.retirement_wife
