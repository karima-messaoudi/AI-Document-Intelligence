from pathlib import Path
from src.ingestion.pdf_loader import extract_text_from_pdf

BASE_DIR = Path(__file__).resolve().parents[2]

pdf_path = BASE_DIR / "data/raw/cv/Karima_Messaoudi_CV.pdf"
text = extract_text_from_pdf(pdf_path)

print(text[:10000])
