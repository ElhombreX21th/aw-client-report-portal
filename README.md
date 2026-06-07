# AW Client Report Portal

A lightweight FastAPI web application for generating client-facing financial planning report summaries and downloadable PDF reports.

The portal collects retirement, asset, liability, cash inflow, and cash outflow values, calculates key financial planning metrics, and generates SACS and TCC PDF report files.

## Overview

**AW Client Report Portal** is designed as a simple reporting prototype for financial planning workflows. It provides a browser-based form where client financial inputs can be reviewed or adjusted, then returns calculated report values and PDF downloads.

Current report outputs include:

- **SACS - Quarterly Cashflow**
- **TCC - Net Worth**

## Features

- FastAPI backend
- Simple client report form
- Retirement account input fields
- Asset and liability input fields
- Cash inflow and outflow calculations
- Net worth calculation
- PDF generation with ReportLab
- In-memory PDF streaming downloads
- Tailwind CSS-based interface

## Tech Stack

- **Python**
- **FastAPI**
- **Uvicorn**
- **ReportLab**
- **Tailwind CSS CDN**
- **HTML / JavaScript**

## Project Structure

```text
aw-client-report-portal/
├── main.py
├── templates/
│   └── index.html
└── README.md
```

> Note: the current application serves the main interface directly from `main.py`. The `templates/index.html` file appears to be an alternate or future template-based version.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ElhombreX21th/aw-client-report-portal.git
cd aw-client-report-portal
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn reportlab python-multipart
```

### 4. Run the application

```bash
python main.py
```

Or run with Uvicorn directly:

```bash
uvicorn main:app --reload
```

### 5. Open in the browser

```text
http://127.0.0.1:8000
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Displays the client report form |
| `POST` | `/generate-reports` | Calculates report metrics from submitted form data |
| `GET` | `/download/sacs` | Downloads the SACS PDF report |
| `GET` | `/download/tcc` | Downloads the TCC PDF report |

## Report Calculations

### Cashflow

```text
Total Inflow = Static Salary + Other Inflow
Total Outflow = Expense Budget + Other Outflow
Excess to Private Reserve = Total Inflow - Total Outflow
```

### Net Worth

```text
Grand Total Net Worth = Retirement Accounts + Non-Retirement Assets + Trust + House Value - Liabilities
```

## Current Demo Data

The current prototype uses hardcoded sample client data:

```python
client = {
    "name": "John & Jane Doe",
    "static_salary": 18500,
    "expense_budget": 9200
}
```

These values should be replaced with real client data sources, environment-based configuration, or database records before production use.

## Production Roadmap

Recommended next steps:

- Move hardcoded client data into a database or secure configuration layer
- Add authentication and authorization
- Add client-specific routing or account selection
- Add validation for financial inputs
- Add tests for calculations and PDF generation
- Move frontend markup out of `main.py` into templates
- Add a `requirements.txt` or `pyproject.toml`
- Add deployment configuration
- Improve PDF layout and branding
- Add export history or audit logging

## Security Notes

This repository currently appears to be a prototype. Before using it with real financial planning data:

- Do not store sensitive client data directly in source code
- Add authentication
- Use HTTPS in production
- Validate all submitted form values
- Keep generated reports private to the authenticated client or advisor
- Avoid committing `.env` files, credentials, tokens, or private client documents

## License

No license file is currently included. Add a license before distributing or reusing this project publicly.

## Author

Created by [ElhombreX21th](https://github.com/ElhombreX21th).
