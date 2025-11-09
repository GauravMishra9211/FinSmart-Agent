import json, uuid, os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models import VerifyRequest, UnderwriteRequest, Decision, SanctionRequest
from utils.sanction import generate_sanction_letter

APP_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(APP_DIR, "data", "customers.json")

with open(DATA_PATH, "r") as f:
    CUSTOMERS = json.load(f)

PHONE_MAP = {c["phone"]: c for c in CUSTOMERS}

app = FastAPI(title="FinSmart Agent API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve sanction PDFs
OUT_DIR = os.path.join(APP_DIR, "out")
os.makedirs(OUT_DIR, exist_ok=True)
app.mount("/files", StaticFiles(directory=OUT_DIR), name="files")

def calc_emi(principal: int, annual_rate: float, months: int) -> float:
    r = annual_rate / 12 / 100.0
    if r == 0:
        return principal / months
    return principal * r * (1 + r) ** months / ((1 + r) ** months - 1)

@app.get("/customers/{phone}")
def get_customer(phone: str):
    cust = PHONE_MAP.get(phone)
    if not cust:
        raise HTTPException(404, "Customer not found")
    return cust

@app.post("/verify")
def verify(req: VerifyRequest):
    cust = PHONE_MAP.get(req.phone)
    if not cust:
        raise HTTPException(404, "Customer not found")
    verified = (req.address is None) or (req.address.lower() in cust["address"].lower())
    return {"verified": verified, "customer": cust}

@app.post("/underwrite", response_model=Decision)
def underwrite(req: UnderwriteRequest):
    cust = PHONE_MAP.get(req.phone)
    if not cust:
        raise HTTPException(404, "Customer not found")

    amount = req.amount
    tenure = req.tenure_months
    rate_pa = 14.0  # demo const
    credit_score = cust["credit_score"]
    pre_limit = cust["preapproved_limit"]
    salary = req.salary or cust["salary"]

    if credit_score < 700:
        return Decision(approved=False, reason="Rejected: Credit score below 700")

    if amount <= pre_limit:
        emi = calc_emi(amount, rate_pa, tenure)
        return Decision(
            approved=True,
            reason="Approved: within pre-approved limit",
            emi=emi,
            rate_pa=rate_pa,
            approval_id=str(uuid.uuid4())[:8],
            customer_id=cust["id"],
            customer_name=cust["name"],
        )

    if amount <= 2 * pre_limit:
        emi = calc_emi(amount, rate_pa, tenure)
        if emi <= 0.5 * salary:
            return Decision(
                approved=True,
                reason="Approved: within 2x limit and EMI ≤ 50% salary",
                emi=emi,
                rate_pa=rate_pa,
                approval_id=str(uuid.uuid4())[:8],
                customer_id=cust["id"],
                customer_name=cust["name"],
            )
        else:
            return Decision(approved=False, reason="Rejected: EMI > 50% salary", emi=emi)

    return Decision(approved=False, reason="Rejected: exceeds 2x pre-approved limit")

@app.post("/sanction")
def sanction(req: SanctionRequest):
    file_name = f"sanction_{req.approval_id}.pdf"
    pdf_path = os.path.join(OUT_DIR, file_name)
    generate_sanction_letter(
        pdf_path,
        req.approval_id,
        req.customer_name,
        req.amount,
        req.tenure_months,
        req.rate_pa,
        req.emi,
    )
    return {"pdf_path": f"files/{file_name}"}

@app.post("/loan/submit")
def loan_submit(payload: dict):
    phone = payload.get("phone")
    amount = int(payload.get("amount"))
    tenure = int(payload.get("tenure_months"))
    address = payload.get("address")
    salary = payload.get("salary")

    # Verify
    v = verify(VerifyRequest(phone=phone, address=address))
    if not v["verified"]:
        return {"stage": "verify", "status": "failed", "reason": "KYC mismatch"}

    # Underwrite
    dec = underwrite(UnderwriteRequest(phone=phone, amount=amount, tenure_months=tenure, salary=salary))
    if not dec.approved:
        return {"stage": "underwrite", "status": "rejected", "reason": dec.reason, "emi": dec.emi}

    # Sanction
    s = sanction(SanctionRequest(
        approval_id=dec.approval_id,
        customer_name=dec.customer_name or "",
        amount=amount,
        tenure_months=tenure,
        rate_pa=dec.rate_pa,
        emi=dec.emi,
    ))
    return {
        "stage": "sanction",
        "status": "approved",
        "approval_id": dec.approval_id,
        "emi": dec.emi,
        "pdf_relative_path": s["pdf_path"]
    }
