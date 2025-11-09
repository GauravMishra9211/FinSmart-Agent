from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_sanction_letter(path, approval_id, customer_name, amount, tenure_months, rate_pa, emi):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    # Header
    c.setFillColorRGB(0.09, 0.2, 0.36)
    c.rect(0, height-40, width, 40, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20, height-28, "FinSmart Agent — Personal Loan Sanction Letter")

    # Body
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 11)
    y = height - 80
    c.drawString(20, y, f"Approval ID: {approval_id}")
    y -= 18
    c.drawString(20, y, f"Date: {datetime.now().strftime('%d-%b-%Y %H:%M')}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, y, "To,")
    y -= 16
    c.setFont("Helvetica", 11)
    c.drawString(20, y, customer_name)
    y -= 28

    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, y, "Subject: Sanction of Personal Loan")
    y -= 24

    c.setFont("Helvetica", 11)
    lines = [
        "We are pleased to inform you that your personal loan application has been approved as per the terms below:",
        f"Sanctioned Amount: INR {amount:,.0f}",
        f"Tenure: {tenure_months} months",
        f"Interest Rate: {rate_pa:.2f}% p.a.",
        f"Monthly EMI: INR {emi:,.2f}",
    ]
    for line in lines:
        c.drawString(20, y, line)
        y -= 18

    y -= 10
    c.drawString(20, y, "This sanction is subject to standard T&C and completion of documentation.")
    y -= 36
    c.drawString(20, y, "Regards,")
    y -= 16
    c.drawString(20, y, "FinSmart Agent — VisionCoders AI")

    c.showPage()
    c.save()
