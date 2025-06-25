import re
from datetime import datetime

def extract_dob_from_text(text):
    # Look for DOB preceded by the keyword
    match = re.search(r'DOB[:\s-]*?(\d{2}[/-]\d{2}[/-]\d{4})', text)
    if match:
        dob_str = match.group(1)
        for fmt in ('%d/%m/%Y', '%d-%m-%Y'):
            try:
                return datetime.strptime(dob_str, fmt)
            except ValueError:
                continue
    # fallback: try generic date match
    match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4})', text)
    if match:
        dob_str = match.group(1)
        for fmt in ('%d/%m/%Y', '%d-%m-%Y'):
            try:
                return datetime.strptime(dob_str, fmt)
            except ValueError:
                continue
    return None
