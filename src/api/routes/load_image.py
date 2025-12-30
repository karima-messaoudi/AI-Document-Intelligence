from fastapi import APIRouter, UploadFile, File, HTTPException
import os, shutil

from src.api import state
from src.ingestion.ocr_loader import extract_text_from_image
from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.chunker import chunk_text
from src.embeddings.embedding_model import load_embedding_model
from src.embeddings.vector_store import build_faiss_index

router = APIRouter(prefix="/load_image", tags=["OCR Image"])

@router.post("")
def load_image(file: UploadFile = File(...)):

    if not file.filename.lower().endswith((".jpg", ".png", ".jpeg")):
        raise HTTPException(400, "Le fichier doit être une image")

    os.makedirs("data/uploaded_images", exist_ok=True)
    path = "data/uploaded_images/current_image.png"

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    raw_text = extract_text_from_image(path)
    if not raw_text.strip():
        raise HTTPException(400, "Texte OCR vide ou illisible")

    clean = clean_text(raw_text)
    chunks = chunk_text(clean)

    embedding_model = load_embedding_model()
    state.vector_store = build_faiss_index(chunks, embedding_model)

    return {"status": "Image OCR indexée avec succès"}
