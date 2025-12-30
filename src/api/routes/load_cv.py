from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from src.api import state
from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.chunker import chunk_text
from src.embeddings.embedding_model import load_embedding_model
from src.embeddings.vector_store import build_faiss_index
from pdfplumber.utils.exceptions import PdfminerException

router = APIRouter(prefix="/load_cv", tags=["CV"])

@router.post("")
def load_cv(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF")

    os.makedirs("data/uploaded_cv", exist_ok=True)
    path = "data/uploaded_cv/current_cv.pdf"

    # 🔁 reset de l’état AVANT chargement
    state.vector_store = None

    try:
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        raw_text = extract_text_from_pdf(path)

        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="PDF vide ou illisible")

        clean = clean_text(raw_text)
        chunks = chunk_text(clean)

        embedding_model = load_embedding_model()
        state.vector_store = build_faiss_index(chunks, embedding_model)

    except PdfminerException:
        state.vector_store = None
        raise HTTPException(status_code=400, detail="PDF invalide ou corrompu")

    except Exception as e:
        state.vector_store = None
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "CV chargé et indexé avec succès"}
