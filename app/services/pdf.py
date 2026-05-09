from __future__ import annotations

from decimal import Decimal
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.models import ClientReportInput
from app.services.calculations import (
    calculate_net_worth,
    calculate_private_reserve,
    calculate_retirement_total,
    calculate_total_inflow,
    calculate_total_outflow,
)


def money(value: Decimal) -> str:
    """Format money consistently for the UI and generated PDFs."""

    return f"${value:,.2f}"


def _draw_centered_text(pdf: canvas.Canvas, x: float, y: float, lines: list[str], font_size: int = 11) -> None:
    pdf.setFillColor(colors.black)
    for index, line in enumerate(lines):
        pdf.setFont("Helvetica-Bold", font_size if index == 0 else max(font_size - 1, 8))
        pdf.drawCentredString(x, y - (index * 13), line)


def _draw_bubble(
    pdf: canvas.Canvas,
    x: float,
    y: float,
    radius: float,
    fill_color: colors.Color,
    lines: list[str],
) -> None:
    pdf.setStrokeColor(colors.HexColor("#172033"))
    pdf.setFillColor(fill_color)
    pdf.circle(x, y, radius, fill=1, stroke=1)
    _draw_centered_text(pdf, x, y + 7, lines)


def build_sacs_pdf(data: ClientReportInput) -> bytes:
    """Build the SACS quarterly cashflow report as PDF bytes."""

    total_inflow = calculate_total_inflow(data)
    total_outflow = calculate_total_outflow(data)
    private_reserve = calculate_private_reserve(data)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setTitle("SACS Quarterly Cashflow")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, height - 72, "SACS - Quarterly Cashflow")
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(width / 2, height - 94, data.client_name)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(width / 2, height - 112, data.quarter)

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(96, height - 165, f"Total Inflow: {money(total_inflow)}")
    pdf.drawString(96, height - 186, f"Total Outflow: {money(total_outflow)}")
    pdf.setFillColor(colors.HexColor("#047857"))
    pdf.drawString(96, height - 217, f"EXCESS TO PRIVATE RESERVE: {money(private_reserve)}")

    _draw_bubble(pdf, 210, 300, 58, colors.HexColor("#A7D8E8"), ["Inflow", money(total_inflow)])
    _draw_bubble(pdf, 402, 300, 58, colors.HexColor("#F07D80"), ["Outflow", money(total_outflow)])
    _draw_bubble(pdf, 306, 186, 74, colors.HexColor("#8BE68B"), ["Private Reserve", money(private_reserve)])

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def build_tcc_pdf(data: ClientReportInput) -> bytes:
    """Build the TCC net worth report as PDF bytes."""

    retirement_total = calculate_retirement_total(data)
    net_worth = calculate_net_worth(data)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setTitle("TCC Net Worth")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, height - 72, "TCC - Net Worth")
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(width / 2, height - 94, data.client_name)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(width / 2, height - 112, data.quarter)

    pdf.setStrokeColor(colors.HexColor("#172033"))
    pdf.circle(width / 2, 284, 145, fill=0, stroke=1)
    _draw_bubble(pdf, width / 2, 395, 74, colors.HexColor("#A7D8E8"), ["Retirement", money(retirement_total)])
    _draw_bubble(pdf, 222, 255, 58, colors.HexColor("#FFAA16"), ["Other Assets", money(data.non_retirement + data.trust + data.house_value)])
    _draw_bubble(pdf, 390, 255, 58, colors.HexColor("#8BE68B"), ["Liabilities", f"- {money(data.liabilities)}"])

    pdf.setFillColor(colors.HexColor("#047857"))
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(width / 2, 150, f"GRAND TOTAL NET WORTH: {money(net_worth)}")

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
