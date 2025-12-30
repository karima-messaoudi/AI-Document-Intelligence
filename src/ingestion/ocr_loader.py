import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\dell\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image introuvable : {image_path}")

    print("🖼️ [OCR] Ouverture de l'image :", image_path)
    image = Image.open(image_path).convert("L")

    # Réduction de taille pour accélérer l'OCR si l'image est énorme
    image.thumbnail((1600, 1600))

    print("🧠 [OCR] Appel à Tesseract...")
    text = pytesseract.image_to_string(image, lang="eng")  # ← pour tester, on met que 'eng'

    print("✅ [OCR] Texte extrait, longueur :", len(text))
    return text
