# FinSmart Agent – AI Driven Personal Loan Sales & Approval System

FinSmart Agent is an **AI-powered Personal Loan Sales Assistant** designed to simplify and automate the loan approval workflow.  
It guides users through a conversational chat interface, verifies KYC, evaluates eligibility (underwriting), calculates EMI, and generates a **PDF sanction letter** automatically.

This project was developed as part of **EY Techathon 6.0 – Challenge II (BFSI Domain)**.

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 🤖 Chat-based Interaction | User applies for loan through a natural chat conversation |
| 🧾 KYC Verification | Checks identity based on stored customer records |
| 📊 Underwriting Logic | Approves/Rejects loan using policy-based financial rules |
| 💰 EMI Calculator | Calculates EMI in real-time using standard banking formula |
| 📄 Sanction Letter PDF | Generates a downloadable PDF approval letter |
| 🌐 Full Stack System | Backend (FastAPI) + Frontend (React + Vite) |

---

## 🏗️ System Workflow

User → Chat UI → Loan Application Form (Conversation)
↓
Backend API (/loan/submit)
↓

KYC Verification

Underwriting Decision (Credit Score, Salary, Limits)

EMI Calculation

Sanction Letter PDF Generation
↓
Approval Result Returned to Chat UI

## 📂 Project Structure

FinSmart/
│
├── backend/
│ ├── app.py # FastAPI Server
│ ├── models.py # Request/Response Schemas
│ ├── utils/
│ │ └── sanction.py # PDF Generator
│ ├── data/
│ │ └── customers.json # Mock Customer KYC Database
│ └── requirements.txt # Python Dependencies
│
└── frontend-react/
├── src/
│ ├── App.jsx
│ ├── main.jsx
│ ├── styles.css
│ └── components/
│ ├── Chat.jsx # Chat Logic + API Calls
│ └── Message.jsx # Chat Message UI Component
├── package.json
├── vite.config.js
└── index.html


---

## ⚙️ Backend Setup (FastAPI)

```bash
cd FinSmart/backend

python -m venv venv

# Windows:
venv\Scripts\activate
# Linux / Mac:
source venv/bin/activate

pip install -r requirements.txt

uvicorn app:app --reload --port 8000

http://localhost:8000
cd FinSmart/frontend-react
npm install
npm run dev
Frontend will run at:

arduino
Copy code
http://localhost:5173

💬 How to Use (Chat Instructions)

Inside the chat UI, type:

start


Then answer the questions:

Phone Number

Loan Amount

Tenure (Months)

City / Address

Salary

If eligible → you will receive:

Loan Approval Result ✅

EMI Amount 💰

PDF Sanction Letter 📄 (Download Link)

🧮 Underwriting Rules Used
Condition	Result
Credit Score < 700	Loan Rejected
Loan ≤ Pre-approved Limit	Auto Approved
Loan ≤ 2× Limit AND EMI ≤ 50% of Salary	Approved
Otherwise	Rejected

EMI Formula:

EMI = P × r × (1+r)^n / ((1+r)^n − 1)

🖼️ Screenshots (Add later)

Create a folder named assets/ and upload your screenshots there.

Chat UI	Loan Approved	PDF Sanction Letter

	
	
🌟 Future Enhancements
Feature	Status
OCR for Document Upload (PAN/Salary Slip)	Coming Soon
Lead Scoring Model (ML/AI)	Planned
WhatsApp/Phone IVR Bot	Future Scope
Multi-language Support	Under Consideration
👥 Team — VisionCoders AI
Name	Role
Gaurav Mishra	Full Stack & AI Integration
Rahul Singh	Backend & Database
Animesh Kumar	Frontend UI/UX
Priya Verma	Business Use Case & Documentation
⭐ Support the Project

If you found this useful, please star the repository on GitHub:

⭐ https://github.com/YOUR-USERNAME/FinSmart-Agent


---

## ✅ Ready to Paste.

Would you like me to:
**(a)** Add a **GitHub banner image** (professional header)  
**(b)** Add GitHub repo description + tags  
**(c)** Generate a **2-minute presentation speech** for jury

Reply: `a`, `b`, `c`, or `all`
