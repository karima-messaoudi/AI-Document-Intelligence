from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from src.ingestion.pdf_loader import extract_text_from_pdf
from src.ingestion.ocr_loader import extract_text_from_image
from src.invoices.invoice_extractor import extract_invoice_data

router = APIRouter(prefix="/invoice", tags=["Invoice"])


@router.post("/analyze")
def analyze_invoice(file: UploadFile = File(...)):
    print("📥 [INVOICE] Fichier reçu :", file.filename)

    filename = file.filename.lower()

    if not any(filename.endswith(ext) for ext in [".pdf", ".jpg", ".jpeg", ".png"]):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF ou une image (jpg/png)")

    os.makedirs("data/invoices", exist_ok=True)
    path = os.path.join("data/invoices", "current_invoice" + os.path.splitext(filename)[1])

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    print(" [INVOICE] Fichier sauvegardé sous :", path)

    # 1. OCR ou PDF → texte
    if filename.endswith(".pdf"):
        print("[INVOICE] Extraction PDF...")
        raw_text = extract_text_from_pdf(path)
    else:
        print(" [INVOICE] OCR image avec Tesseract...")
        raw_text = extract_text_from_image(path)

    print(" [INVOICE] Longueur texte OCR :", len(raw_text))

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Impossible d'extraire du texte de cette facture")

    # 2. Extraction structurée
    print(" [INVOICE] Extraction des champs structurés...")
    structured = extract_invoice_data(raw_text)
    print(" [INVOICE] Extraction terminée :", structured)

    return {
        "status": "OK",
        "structured": structured,
        "raw_text_preview": raw_text[:800]
    }
