# pdf_parser
|| Credit Card Statement PDF Parser
|| Overview

This project is a Credit Card Statement Parser built using Python.
It automatically extracts key information (like card number, balance, and due date) from credit card statements in PDF format, supporting multiple banks and formats — including scanned PDFs using OCR (Optical Character Recognition).

It can be run via the command line or through an interactive Streamlit web app.

**Features**

**Extracts 5 key data points:**

1. Card last 4 digits

2. Card type/variant

3. Billing cycle / statement period

4. Payment due date

5. Total balance

**What it does is:**

1. Supports multiple banks (e.g. HDFC, SBI, Axis, ICICI, Amex)

2. Uses regex + OCR (Tesseract) for accurate text extraction

3. Includes Streamlit web interface for easy uploads

4. Outputs extracted data in structured JSON format

**Project Structure**
cc-stmt-parser/
│
├── parser.py               # Core PDF parsing logic
├── app.py                  # Streamlit web interface
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── samples/                # Sample PDF statements
│   ├── fake_bank_statement.pdf
│   └── ...
├── outputs/
│   └── extracted_data.json
└── venv/ (optional)        # Virtual environment

**Installation**
1. Clone the Repository
git clone https://github.com/asmgit19/pdf_parser.git
cd pdf_parser

**2. Create Virtual Environment**
python -m venv venv
venv\Scripts\activate

**3. Install Dependencies**
pip install -r requirements.txt

**4. Install Tesseract OCR**
Download and install Tesseract OCR (for scanned PDFs):
🔗 Tesseract for Windows

Then update its path inside parser.py if needed:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

**Usage**
Option 1: Run via Command Line
python parser.py .\samples\fake_bank_statement.pdf .\outputs\extracted_data.json


**Output example:**

{
  "card_last4": "1234",
  "card_variant": "Visa Platinum",
  "billing_cycle": "Oct 01, 2025 - Oct 31, 2025",
  "payment_due_date": "2025-11-20",
  "total_balance": "2345.00"
}

Option 2: Run via Streamlit Web App
streamlit run app.py


Upload a statement PDF → View extracted data instantly!

**Tech Stack**

Python 3.11+

pdfplumber – PDF text extraction

pytesseract – OCR for scanned statements

regex / re – Pattern-based field extraction

Streamlit – Web-based UI

dateutil – Smart date parsing

**Example Output Screenshot**
(Add screenshot of Streamlit app running or console output here)

**Author**

**Anjali Mishra** (GitHub: asmgit19
)
Built as part of a company assignment round — demonstrating real-world PDF parsing and data extraction skills.
