from decimal import Decimal

import pytest

from app.models import ClientReportInput
from app.services.calculations import (
    calculate_net_worth,
    calculate_private_reserve,
    calculate_total_inflow,
    calculate_total_outflow,
)


def test_cashflow_calculations_use_all_inflow_and_outflow_fields():
    data = ClientReportInput(other_inflow=Decimal("500"), other_outflow=Decimal("250"))

    assert calculate_total_inflow(data) == Decimal("19000")
    assert calculate_total_outflow(data) == Decimal("10250")
    assert calculate_private_reserve(data) == Decimal("8750")


def test_net_worth_calculation_matches_assessment_formula():
    data = ClientReportInput()

    assert calculate_net_worth(data) == Decimal("1930000")


def test_money_formatter_keeps_cents_and_grouping():
    pytest.importorskip("reportlab")
    from app.services.pdf import money

    assert money(Decimal("1930000")) == "$1,930,000.00"


def test_pdf_builders_return_pdf_documents():
    pytest.importorskip("reportlab")
    from app.services.pdf import build_sacs_pdf, build_tcc_pdf

    data = ClientReportInput()

    assert build_sacs_pdf(data).startswith(b"%PDF")
    assert build_tcc_pdf(data).startswith(b"%PDF")
