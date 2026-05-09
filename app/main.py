from __future__ import annotations

from dataclasses import fields
from decimal import Decimal, InvalidOperation
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import ClientReportInput
from app.services.calculations import calculate_net_worth, calculate_private_reserve
from app.services.pdf import build_sacs_pdf, build_tcc_pdf, money

app = FastAPI(
    title="AW Client Report Portal",
    description="Automated SACS cashflow and TCC net worth report generator.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    """Render the pre-populated quarterly report form."""

    data = ClientReportInput()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": data,
            "generated": False,
            "private_reserve": None,
            "net_worth": None,
            "query_params": {},
        },
    )


@app.post("/reports/generate", response_class=HTMLResponse)
def generate_reports(
    request: Request,
    client_name: Annotated[str, Form()],
    quarter: Annotated[str, Form()],
    retirement_husband: Annotated[Decimal, Form()],
    retirement_wife: Annotated[Decimal, Form()],
    non_retirement: Annotated[Decimal, Form()],
    trust: Annotated[Decimal, Form()],
    house_value: Annotated[Decimal, Form()],
    liabilities: Annotated[Decimal, Form()],
    salary_income: Annotated[Decimal, Form()],
    social_security: Annotated[Decimal, Form()],
    pension_income: Annotated[Decimal, Form()],
    other_inflow: Annotated[Decimal, Form()],
    mortgage: Annotated[Decimal, Form()],
    taxes: Annotated[Decimal, Form()],
    living_expenses: Annotated[Decimal, Form()],
    insurance: Annotated[Decimal, Form()],
    other_outflow: Annotated[Decimal, Form()],
) -> HTMLResponse:
    """Calculate report totals and show direct PDF download links."""

    data = ClientReportInput(
        client_name=client_name,
        quarter=quarter,
        retirement_husband=retirement_husband,
        retirement_wife=retirement_wife,
        non_retirement=non_retirement,
        trust=trust,
        house_value=house_value,
        liabilities=liabilities,
        salary_income=salary_income,
        social_security=social_security,
        pension_income=pension_income,
        other_inflow=other_inflow,
        mortgage=mortgage,
        taxes=taxes,
        living_expenses=living_expenses,
        insurance=insurance,
        other_outflow=other_outflow,
    )
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": data,
            "generated": True,
            "private_reserve": money(calculate_private_reserve(data)),
            "net_worth": money(calculate_net_worth(data)),
            "query_params": data.to_query_params(),
        },
    )


@app.get("/reports/sacs")
def download_sacs(request: Request) -> Response:
    """Download a SACS cashflow PDF generated from query parameters."""

    data = _data_from_query(request)
    return Response(
        build_sacs_pdf(data),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="SACS_Report.pdf"'},
    )


@app.get("/reports/tcc")
def download_tcc(request: Request) -> Response:
    """Download a TCC net worth PDF generated from query parameters."""

    data = _data_from_query(request)
    return Response(
        build_tcc_pdf(data),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="TCC_Net_Worth.pdf"'},
    )


def _data_from_query(request: Request) -> ClientReportInput:
    values: dict[str, object] = {}
    defaults = ClientReportInput()

    for field in fields(ClientReportInput):
        raw_value = request.query_params.get(field.name, str(getattr(defaults, field.name)))
        if field.type == "str":
            values[field.name] = raw_value
            continue

        try:
            values[field.name] = Decimal(raw_value)
        except (InvalidOperation, ValueError) as exc:
            raise HTTPException(status_code=422, detail=f"Invalid decimal value for {field.name}") from exc

    return ClientReportInput(**values)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
