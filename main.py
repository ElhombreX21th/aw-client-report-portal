from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO

app = FastAPI(title="AW Client Report Portal")

client = {
    "name": "John & Jane Doe",
    "static_salary": 18500,
    "expense_budget": 9200
}

# ====================== HTML ======================
HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AW Client Report Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen py-8">
    <div class="max-w-4xl mx-auto px-6">
        <h1 class="text-4xl font-bold text-center text-gray-800 mb-2">AW Client Report Portal</h1>
        <p class="text-center text-gray-600 mb-10">EF Financial Planning • """ + client["name"] + """</p>

        <form id="reportForm" class="bg-white shadow-2xl rounded-3xl p-10">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                    <h3 class="font-semibold text-lg mb-4 text-blue-700">Retirement Accounts</h3>
                    <div class="space-y-4">
                        <div><label class="block text-sm font-medium">Husband</label><input type="number" name="retirement_husband" value="450000" class="w-full border border-gray-300 rounded-xl px-4 py-3"></div>
                        <div><label class="block text-sm font-medium">Wife</label><input type="number" name="retirement_wife" value="320000" class="w-full border border-gray-300 rounded-xl px-4 py-3"></div>
                    </div>
                </div>
                <div>
                    <h3 class="font-semibold text-lg mb-4 text-emerald-700">Other Assets & Liabilities</h3>
                    <div class="space-y-4">
                        <div><label class="block text-sm font-medium">Non-Retirement</label><input type="number" name="non_retirement" value="180000" class="w-full border border-gray-300 rounded-xl px-4 py-3"></div>
                        <div><label class="block text-sm font-medium">Trust</label><input type="number" name="trust" value="250000" class="w-full border border-gray-300 rounded-xl px-4 py-3"></div>
                        <div><label class="block text-sm font-medium">House Value (Zillow)</label><input type="number" name="house_value" value="850000" class="w-full border border-gray-300 rounded-xl px-4 py-3"></div>
                        <div><label class="block text-sm font-medium">Liabilities</label><input type="number" name="liabilities" value="120000" class="w-full border border-gray-300 rounded-xl px-4 py-3"></div>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-6 mt-8">
                <div><label class="block text-sm font-medium">Other Inflow</label><input type="number" name="inflow_other" value="0" class="w-full border border-gray-300 rounded-xl px-4 py-3"></div>
                <div><label class="block text-sm font-medium">Other Outflow</label><input type="number" name="outflow_other" value="0" class="w-full border border-gray-300 rounded-xl px-4 py-3"></div>
            </div>

            <button type="submit" class="mt-10 w-full bg-gradient-to-r from-blue-600 to-emerald-600 text-white font-bold py-6 rounded-2xl text-xl">Generate SACS + TCC Reports</button>
        </form>

        <div id="results" class="mt-8"></div>
    </div>

    <script>
        document.getElementById('reportForm').onsubmit = async (e) => {
            e.preventDefault();
            const form = new FormData(e.target);
            const res = await fetch('/generate-reports', {method: 'POST', body: form});
            if (!res.ok) {
                alert("Erro ao gerar relatórios");
                return;
            }
            const data = await res.json();

            document.getElementById('results').innerHTML = `
                <div class="bg-white shadow-2xl rounded-3xl p-10 text-center">
                    <h2 class="text-3xl font-bold text-emerald-600 mb-6">✅ Reports Generated Successfully!</h2>
                    <p class="text-2xl">Excess to Private Reserve: <strong>$${data.excess_reserve.toLocaleString()}</strong></p>
                    <p class="text-2xl mb-8">Grand Total Net Worth: <strong>$${data.grand_total.toLocaleString()}</strong></p>
                    <a href="/download/sacs" class="inline-block bg-blue-600 text-white px-8 py-4 rounded-2xl mr-4 hover:bg-blue-700">↓ Download SACS PDF</a>
                    <a href="/download/tcc" class="inline-block bg-emerald-600 text-white px-8 py-4 rounded-2xl hover:bg-emerald-700">↓ Download TCC PDF</a>
                </div>
            `;
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_CONTENT

# PDF Generation in Memory
def generate_sacs_pdf(buffer, data):
    c = canvas.Canvas(buffer, pagesize=letter)
    w, h = letter
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w/2, h-60, "SACS - Quarterly Cashflow")
    c.drawCentredString(w/2, h-90, data["client_name"])
    c.setFont("Helvetica-Bold", 14)
    c.drawString(80, h-160, f"Total Inflow: ${data['inflow']:,.2f}")
    c.drawString(80, h-190, f"Total Outflow: ${data['outflow']:,.2f}")
    c.setFillColor(colors.green)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(80, h-230, f"EXCESS TO PRIVATE RESERVE: ${data['excess']:,.2f}")
    c.save()

def generate_tcc_pdf(buffer, data):
    c = canvas.Canvas(buffer, pagesize=letter)
    w, h = letter
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w/2, h-60, "TCC - Net Worth")
    c.drawCentredString(w/2, h-90, data["client_name"])
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w/2, 130, f"GRAND TOTAL: ${data['grand_total']:,.2f}")
    c.save()

@app.post("/generate-reports")
async def generate_reports(
    retirement_husband: float = Form(...),
    retirement_wife: float = Form(...),
    non_retirement: float = Form(...),
    trust: float = Form(...),
    house_value: float = Form(...),
    liabilities: float = Form(...),
    inflow_other: float = Form(0),
    outflow_other: float = Form(0)
):
    inflow = client["static_salary"] + inflow_other
    outflow = client["expense_budget"] + outflow_other
    excess = inflow - outflow
    total_ret = retirement_husband + retirement_wife
    grand_total = total_ret + non_retirement + trust + house_value - liabilities

    return {
        "excess_reserve": excess,
        "grand_total": grand_total
    }

@app.get("/download/sacs")
async def download_sacs():
    buffer = BytesIO()
    data = {"client_name": client["name"], "inflow": 18500, "outflow": 9200, "excess": 9300}
    generate_sacs_pdf(buffer, data)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=SACS_Report.pdf"})

@app.get("/download/tcc")
async def download_tcc():
    buffer = BytesIO()
    data = {"client_name": client["name"], "grand_total": 1930000}
    generate_tcc_pdf(buffer, data)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=TCC_Net_Worth.pdf"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)