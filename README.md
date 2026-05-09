# AW Client Report Portal

A modern, automated web portal that allows a small financial planning team to generate polished quarterly **SACS (Cashflow)** and **TCC (Net Worth)** reports in minutes instead of a full day.

Built as part of the AI Automation Engineer technical assessment for Sagan (2026).

---

## 🎯 Problem Solved

The EF Financial Planning team currently spends **one full day per client** manually collecting data from multiple sources (Schwab, Pinnacle Bank, Zillow, RightCapital), performing calculations, and assembling reports in Canva/Word. This project eliminates that bottleneck by centralizing data entry, automating calculations, and generating downloadable PDFs.

## ✨ Key Features

- **One-time-style client setup form** with pre-populated sample data.
- **Quarterly cashflow entry** for income and expense categories.
- **Automated calculations**:
  - Total inflow.
  - Total outflow.
  - Excess to private reserve.
  - Total net worth: retirement + non-retirement + trust + house value - liabilities.
- **Professional PDF generation**:
  - SACS cashflow report with inflow, outflow, and private reserve bubbles.
  - TCC net worth report with a circle diagram and grand total.
- Clean, responsive UI optimized for small teams.
- Direct PDF downloads.

## 🛠 Tech Stack

- **Backend:** Python + FastAPI
- **Frontend:** HTML + Tailwind CSS CDN + small custom CSS file
- **Templates:** Jinja2
- **PDF Generation:** ReportLab
- **Deployment:** Railway-ready via `Procfile`

## 📁 Project Structure

```text
aw-client-report-portal/
├── app/
│   ├── main.py                  # FastAPI routes and form/PDF endpoints
│   ├── models.py                # Report input dataclass
│   ├── services/
│   │   ├── calculations.py      # Cashflow and net worth formulas
│   │   └── pdf.py               # SACS and TCC PDF builders
│   ├── static/
│   │   └── styles.css           # Small custom UI styles
│   └── templates/
│       └── index.html           # Main data-entry page
├── tests/
│   └── test_calculations.py     # Calculation and PDF smoke tests
├── Procfile                     # Railway start command
├── requirements.txt             # Python dependencies
└── README.md
```

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd aw-client-report-portal

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python -m app.main
```

Open the app at: <http://127.0.0.1:8000>

## ✅ Run Tests

```bash
pytest
```

## 🧾 Report Workflow

1. Open the portal.
2. Review or update the client, quarter, cashflow, asset, and liability fields.
3. Click **Generate SACS + TCC Reports**.
4. Review the calculated private reserve and net worth totals.
5. Download the SACS and TCC PDFs.

## ☁️ Railway Deployment

1. Push this repository to GitHub.
2. Create a new Railway project from the GitHub repository.
3. Railway will install `requirements.txt` and use the `Procfile` command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## 📸 Screenshots

Add screenshots of the UI and generated PDFs here after deployment or local QA.
