from pathlib import Path
from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.text_cleaner import clean_text

BASE_DIR = Path(__file__).resolve().parents[2]
pdf_path = BASE_DIR / "data/raw/cv/Karima_Messaoudi_CV.pdf"

raw_text = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(raw_text)

print(cleaned_text[:10000])
