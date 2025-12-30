import re

def clean_text(text: str) -> str:
    # Supprimer caractères PDF bizarres
    text = re.sub(r"\(cid:\d+\)", " ", text)

    # Corriger accents cassés (espaces parasites)
    text = re.sub(r"\s+([àâäéèêëîïôöùûüç])", r"\1", text, flags=re.IGNORECASE)

    # Corriger emails cassés
    text = re.sub(r"\s*@\s*", "@", text)
    text = re.sub(r"\s*\.\s*", ".", text)

    # Normaliser séparateurs
    text = re.sub(r"[•|#]", " - ", text)
    text = re.sub(r"[–—]", "-", text)

    # Séparer mots collés (minuscule → majuscule)
    text = re.sub(r"([a-zà-ÿ])([A-ZÀ-Ÿ])", r"\1 \2", text)

    # Séparer lettre/chiffre
    text = re.sub(r"([A-Za-z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([A-Za-z])", r"\1 \2", text)

    # Corriger mots très fréquents collés (FR)
    text = re.sub(r"(et)([A-ZÀ-Ÿa-zà-ÿ])", r"\1 \2", text)
    text = re.sub(r"(de)([A-ZÀ-Ÿa-zà-ÿ])", r"\1 \2", text)

    # Ajouter retours à la ligne avant sections importantes
    sections = [
        "Formations",
        "Expérience Professionnelle",
        "Projets",
        "Compétences",
        "Langues"
    ]
    for section in sections:
        text = re.sub(section, f"\n\n{section}\n", text)

    # Nettoyer espaces multiples
    text = re.sub(r"\s+", " ", text)

    return text.strip()
