import os
import re
import json
from dateutil.parser import parse as parse_dt

import pdfplumber
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

RE_LAST4 = re.compile(r'(?:ending in|ending|Acct(?:\.|ount)?(?: no)?\.?|Account ending)\s*[:\-]?\s*(?:\*+)?(\d{4})', re.I)
RE_BALANCE = re.compile(r'(?:New Balance|Total Due|Amount Due|Balance Due|Total Balance)[:\s\$\n\-]*([-\$,\d\.]+)', re.I)
RE_DUE_DATE = re.compile(r'(?:Payment Due Date|Due Date|Pay by)[:\s]*([A-Za-z0-9,\/\.\- ]{6,40})', re.I)
RE_STATEMENT_PERIOD = re.compile(r'(?:Statement Period|Billing Period|Statement Date)[:\s]*([A-Za-z0-9,\/\-\s]+(?:to|-)[A-Za-z0-9,\/\-\s]+)', re.I)
RE_CARD_NAME = re.compile(r'(?:Card Type|Account Type|Card)\s*[:\-\n]?\s*([A-Za-z0-9\-\s]+(?:Card|Visa|Mastercard|Amex|American Express|Sapphire|Platinum)?)', re.I)

def text_from_pdf(path):
    """Return (full_text, pages_text_list). Uses pdfplumber text extraction, OCR fallback if page empty."""
    pages_text = []
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            txt = p.extract_text()
            if txt and txt.strip():
                pages_text.append(txt)
            else:
                
                img = p.to_image(resolution=300).original
                ocr = pytesseract.image_to_string(img)
                pages_text.append(ocr)
    return "\n\n".join(pages_text), pages_text

def first_match(pattern, text):
    m = pattern.search(text)
    return m.group(1).strip() if m else None

def normalize_amount(s):
    if not s:
        return None
    s2 = s.replace("$","").replace(",","").strip()
    try:
        return f"{float(s2):.2f}"
    except:
        return s.strip()

def extract_fields(full_text):
    out = {}
    out['card_last4'] = first_match(RE_LAST4, full_text)
    out['card_variant'] = first_match(RE_CARD_NAME, full_text)
    out['billing_cycle'] = first_match(RE_STATEMENT_PERIOD, full_text)
    due_raw = first_match(RE_DUE_DATE, full_text)
    if due_raw:
        try:
            out['payment_due_date'] = parse_dt(due_raw, fuzzy=True).date().isoformat()
        except:
            out['payment_due_date'] = due_raw
    else:
        out['payment_due_date'] = None
    bal_raw = first_match(RE_BALANCE, full_text)
    out['total_balance'] = normalize_amount(bal_raw)
    return out

def parse_and_save(input_path, save_to=None):
    full, pages = text_from_pdf(input_path)
    extracted = extract_fields(full)
    
    extracted['_file'] = os.path.basename(input_path)
    extracted['_sample_text_snippet'] = (pages[0][:400] if pages else "")  
    if save_to:
        
        if save_to.endswith('.json'):
            
            data = []
            if os.path.exists(save_to):
                try:
                    with open(save_to, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except:
                    data = []
            data.append(extracted)
            with open(save_to, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        else:
            
            with open(save_to, 'a', encoding='utf-8') as f:
                f.write(json.dumps(extracted, ensure_ascii=False) + "\n")
    return extracted

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python parser.py <pdf-path> [output-json]")
        sys.exit(1)
    input_pdf = sys.argv[1]
    outpath = sys.argv[2] if len(sys.argv) > 2 else os.path.join("outputs", "extracted_data.json")
    if not os.path.exists(input_pdf):
        print("Input file not found:", input_pdf); sys.exit(1)
    result = parse_and_save(input_pdf, save_to=outpath)
    print(json.dumps(result, indent=2, ensure_ascii=False))
