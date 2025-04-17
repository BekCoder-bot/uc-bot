import pytesseract
from PIL import Image
import re

def extract_payment_info(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        summa_match = re.search(r'(\d{2,3}(?:[ ,]?\d{3})*)\s*so?m', text, re.IGNORECASE)
        amount = summa_match.group(1).replace(' ', '').replace(',', '') if summa_match else None

        date_match = re.search(r'(\d{1,2}[:.]\d{2}(?:[:.]\d{2})?)', text)
        time = date_match.group(1) if date_match else None

        return {
            "amount": amount,
            "time": time,
            "raw_text": text
        }
    except Exception as e:
        return {"error": str(e)}
