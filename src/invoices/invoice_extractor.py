import re


def _search(pattern: str, text: str):
    """
    Utilitaire : renvoie le 1er groupe capturé ou None.
    """
    m = re.search(pattern, text, flags=re.IGNORECASE)
    return m.group(1).strip() if m else None


def _search_many(patterns, text: str):
    """
    Essaie plusieurs regex et renvoie la 1ère qui matche.
    """
    for p in patterns:
        m = re.search(p, text, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).strip()
    return None


def _normalize_number(s: str | None) -> str | None:
    """
    Nettoie un montant :
    - supprime les espaces
    - garde les virgules
    """
    if not s:
        return None
    s = s.replace("€", "").strip()
    s = re.sub(r"\s+", "", s)
    return s + "€"


def _extract_vendor(raw_text: str) -> str | None:
    """
    Heuristique pour le fournisseur :
    - on prend les lignes avant 'FACTURE'
    - on choisit la ligne la plus 'probable'
    """
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    # on coupe au niveau de FACTURE
    facture_idx = None
    for i, line in enumerate(lines):
        if "facture" in line.lower():
            facture_idx = i
            break

    header_lines = lines[:facture_idx] if facture_idx is not None else lines[:8]

    if not header_lines:
        return None

    # On filtre les lignes trop courtes (genre "Ta")
    candidates = [l for l in header_lines if len(l) >= 3]

    if not candidates:
        return None

    # scoring simple : on favorise les lignes en MAJUSCULES ou "joli nom"
    def score(line: str) -> int:
        s = 0
        if line.isupper():
            s += 2
        if 2 <= len(line.split()) <= 4:
            s += 1
        return s

    best = max(candidates, key=score)
    return best


def extract_invoice_data(raw_text: str) -> dict:
    """
    Extraction robuste des champs principaux d'une facture.
    """

    # Version "flat" pour faciliter les regex
    flat = raw_text.replace("\n", " ")
    flat = re.sub(r"\s+", " ", flat)

    # ---------------- N° de facture ----------------
    invoice_number = _search(
        r"FACTURE\s*(?:N°|NO|N)\s*[:\-]?\s*([A-Z0-9\-\/]+)",
        flat,
    )

    # ---------------- Date ----------------
    date = _search(
        r"DATE\s*[:\-]?\s*(\d{2}\s*/\s*\d{2}\s*/\s*\d{4})",
        flat,
    )

    # ---------------- Total HT ----------------
    total_ht_raw = _search_many(
        [
            r"TOTAL\s+HT\s*[:\-]?\s*([\d\s\.]+[,\.][0-9]{2}\s*€?)",
            r"HT\s*[:\-]?\s*([\d\s\.]+[,\.][0-9]{2}\s*€?)",
        ],
        flat,
    )
    total_ht = _normalize_number(total_ht_raw)

    # ---------------- TVA montant + taux ----------------
    tva_amount_raw = _search_many(
        [
            r"TVA\s*(?:[0-9]{1,2}\s*%?)?\s*[:\-]?\s*([\d\s\.]+[,\.][0-9]{2}\s*€?)",
            r"TVA\s*[0-9]{1,2}\s*%\s*[:\-]?\s*([\d\s\.]+[,\.][0-9]{2}\s*€?)",
        ],
        flat,
    )
    tva_amount = _normalize_number(tva_amount_raw)

    tva_rate = _search(
        r"TVA\s*([0-9]{1,2})\s*%",
        flat,
    )

    # ---------------- Total TTC ----------------
    total_ttc_raw = _search_many(
        [
            r"TOTAL\s+TTC\s*[:\-]?\s*([\d\s\.]+[,\.][0-9]{2}\s*€?)",
            r"TOTALTTC\s*[:\-]?\s*([\d\s\.]+[,\.][0-9]{2}\s*€?)",
            r"TTC\s*[:\-]?\s*([\d\s\.]+[,\.][0-9]{2}\s*€?)",
        ],
        flat,
    )
    total_ttc = _normalize_number(total_ttc_raw)

    # ---------------- Devise ----------------
    currency = None
    if "€" in raw_text:
        currency = "EUR"
    elif "$" in raw_text:
        currency = "USD"

    # ---------------- Fournisseur ----------------
    vendor = _extract_vendor(raw_text)

    return {
        "vendor": vendor,
        "invoice_number": invoice_number,
        "date": date,
        "total_ht": total_ht,
        "tva_amount": tva_amount,
        "tva_rate": tva_rate,
        "total_ttc": total_ttc,
        "currency": currency,
        "raw_text": raw_text,  # utile pour debug/affichage
    }
