from pathlib import Path
from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.chunker import chunk_text

BASE_DIR = Path(__file__).resolve().parents[2]
pdf_path = BASE_DIR / "data/raw/cv/Karima_Messaoudi_CV.pdf"

text = extract_text_from_pdf(pdf_path)
text = clean_text(text)

chunks = chunk_text(text)

print(f"\nNombre total de chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks):
    print("=" * 80)
    print(f"CHUNK {i+1} (longueur: {len(chunk)} caractères)\n")
    print(chunk)
    print("\n")



