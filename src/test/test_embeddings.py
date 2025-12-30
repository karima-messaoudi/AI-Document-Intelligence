from pathlib import Path

from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.chunker import chunk_text
from src.embeddings.embedding_model import load_embedding_model
from src.embeddings.vector_store import build_faiss_index

# Charger document
BASE_DIR = Path(__file__).resolve().parents[2]
pdf_path = BASE_DIR / "data/raw/cv/Karima_Messaoudi_CV.pdf"

text = extract_text_from_pdf(pdf_path)
text = clean_text(text)
chunks = chunk_text(text)

# Embeddings via OpenAI
embedding_model = load_embedding_model()
vector_store = build_faiss_index(chunks, embedding_model)

# Recherche sémantique
query = "Liste uniquement les compétences explicitement mentionnées"
results = vector_store.similarity_search(query, k=3)

print("\nRésultats de recherche sémantique:\n")
for r in results:
    print("-" * 50)
    print(r.page_content)
