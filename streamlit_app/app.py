import streamlit as st
import requests

# =========================
# CONFIGURATION PAGE
# =========================
st.set_page_config(
    page_title="Document Intelligence (CV & Factures)",
    layout="wide"
)

st.title("📑 Document Intelligence : CV & Factures")
st.caption("Analyse intelligente de CV (RAG) + Extraction automatique de factures (OCR)")

# =========================
# API ENDPOINTS
# =========================
API_LOAD_CV = "http://127.0.0.1:8000/load_cv"
API_CHAT = "http://127.0.0.1:8000/chat"
API_INVOICE = "http://127.0.0.1:8000/invoice/analyze"

# =========================
# SESSION STATE
# =========================
if "history_cv" not in st.session_state:
    st.session_state.history_cv = []

if "cv_uploaded" not in st.session_state:
    st.session_state.cv_uploaded = False

if "history_invoice" not in st.session_state:
    st.session_state.history_invoice = []

# =========================
# SIDEBAR — MODE
# =========================
st.sidebar.header("⚙️ Mode")
mode = st.sidebar.radio(
    "Choisir un mode :",
    ["Analyse de CV", "Analyse de facture"],
    index=0
)

# =========================
# MODE 1 : ANALYSE DE CV (RAG)
# =========================
if mode == "Analyse de CV":
    st.subheader("📄 Analyse intelligente de CV (RAG)")
    st.caption("Charge un CV, puis pose des questions factuelles dessus.")

    # ---------- UPLOAD CV ----------
    st.sidebar.markdown("### 📎 Chargement du CV")

    uploaded_cv = st.sidebar.file_uploader(
        "Uploader un CV (PDF)",
        type=["pdf"],
        key="cv_uploader"
    )

    if uploaded_cv and st.sidebar.button("📥 Indexer le CV"):
        st.sidebar.info("Indexation du CV en cours...")

        try:
            response = requests.post(
                API_LOAD_CV,
                files={
                    "file": (
                        uploaded_cv.name,
                        uploaded_cv.getvalue(),
                        "application/pdf"
                    )
                },
                timeout=60
            )

            if response.status_code == 200:
                st.sidebar.success("CV indexé avec succès ✅")
                st.session_state.cv_uploaded = True
                st.session_state.history_cv = []  # reset historique
            else:
                st.sidebar.error(response.json().get("detail", "Erreur API lors de l’indexation."))

        except Exception as e:
            st.sidebar.error(f"Erreur lors de l’appel à l’API : {e}")

    # ---------- QUESTION INPUT ----------
    st.markdown("### ❓ Poser une question sur le CV")

    question = st.text_input(
        "",
        placeholder="Ex : Dans quelle université le candidat a-t-il fait son master ?",
        key="cv_question_input"
    )

    if st.button("🔍 Analyser le CV", use_container_width=True):

        if not st.session_state.cv_uploaded:
            st.warning("Veuillez d'abord charger et indexer un CV.")
        elif not question.strip():
            st.warning("Veuillez saisir une question.")
        else:
            try:
                with st.spinner("🧠 Analyse du CV en cours..."):
                    response = requests.post(
                        API_CHAT,
                        json={"question": question},
                        timeout=60
                    )

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.history_cv.append({
                        "question": question,
                        "answer": data.get("answer", ""),
                        "sources": data.get("sources", [])
                    })
                else:
                    st.error("Erreur lors de l’appel à l’API /chat")

            except Exception as e:
                st.error(f"Erreur API : {e}")

    # ---------- HISTORY DISPLAY ----------
    st.divider()
    st.subheader("🧠 Historique des questions (CV)")

    if not st.session_state.history_cv:
        st.info("Aucune question posée pour le moment.")
    else:
        for i, item in enumerate(reversed(st.session_state.history_cv), 1):
            st.markdown(f"### Question {i}")
            st.markdown(f"**❓ {item['question']}**")
            st.success(item["answer"])

            if item["sources"]:
                with st.expander("📚 Sources utilisées"):
                    for src in item["sources"]:
                        st.write("•", src)

# =========================
# MODE 2 : ANALYSE DE FACTURE (OCR)
# =========================
else:
    st.subheader("🧾 Analyse de facture (OCR + extraction)")
    st.caption("Uploader une facture (image ou PDF), puis extraire automatiquement les montants & infos clés.")

    # ---------- UPLOAD FACTURE ----------
    st.sidebar.markdown("### 🧾 Chargement de la facture")

    invoice_file = st.sidebar.file_uploader(
        "Uploader une facture (PDF ou image)",
        type=["pdf", "png", "jpg", "jpeg"],
        key="invoice_uploader"
    )

    # Zone principale
    col_left, col_right = st.columns([1.1, 1])

    with col_left:
        st.markdown("### 1️⃣ Facture à analyser")
        if invoice_file is None:
            st.info("Aucune facture chargée pour l’instant. Uploade un fichier à gauche pour commencer.")
        else:
            # Aperçu
            if invoice_file.type.startswith("image/"):
                st.image(
                    invoice_file.getvalue(),
                    caption=f"Aperçu de la facture : {invoice_file.name}",
                    use_container_width=True
                )
            else:
                st.info(f"📄 Fichier PDF détecté : **{invoice_file.name}** (aperçu non disponible)")

    with col_right:
        st.markdown("### 2️⃣ Résultat de l’analyse")

        # Placeholder pour afficher les résultats APRES traitement
        result_container = st.empty()

        # Bouton lancer analyse
        if st.button("📡 Analyser la facture", use_container_width=True):

            if invoice_file is None:
                st.warning("Veuillez d'abord uploader une facture.")
            else:
                try:
                    with st.spinner("📡 Analyse de la facture en cours (OCR + extraction des champs)…"):
                        response = requests.post(
                            API_INVOICE,
                            files={
                                "file": (
                                    invoice_file.name,
                                    invoice_file.getvalue(),
                                    invoice_file.type
                                )
                            },
                            timeout=120  # facture + OCR peut être un peu long
                        )

                    if response.status_code == 200:
                        data = response.json()
                        structured = data.get("structured", {})
                        raw_preview = data.get("raw_text_preview", "")

                        st.session_state.history_invoice.append({
                            "file_name": invoice_file.name,
                            "structured": structured,
                            "raw_text_preview": raw_preview
                        })

                        # Affichage dans le placeholder
                        with result_container.container():
                            st.success("✅ Analyse terminée")

                            if structured:
                                st.markdown("#### 🧾 Champs extraits")

                                c1, c2 = st.columns(2)
                                with c1:
                                    st.write("**Fournisseur :**", structured.get("vendor", "—"))
                                    st.write("**N° facture :**", structured.get("invoice_number", "—"))
                                    st.write("**Date :**", structured.get("date", "—"))
                                with c2:
                                    st.write("**Total HT :**", structured.get("total_ht", "—"))
                                    st.write("**TVA (montant) :**", structured.get("tva", "—"))
                                    st.write("**TVA (%) :**", structured.get("tva_rate", "—"))
                                    st.write("**Total TTC :**", structured.get("total_ttc", "—"))
                                    st.write("**Devise :**", structured.get("currency", "—"))

                            

                    else:
                        try:
                            detail = response.json().get("detail", "Erreur inconnue côté API")
                        except Exception:
                            detail = "Erreur inconnue côté API"
                        st.error(f"Erreur API /invoice/analyze : {detail}")

                except requests.exceptions.ReadTimeout:
                    st.error("⏱️ L’analyse a pris trop de temps (timeout). Essaie avec une image plus légère ou une facture plus simple.")
                except Exception as e:
                    st.error(f"Erreur lors de l’appel à l’API : {e}")

    # ---------- HISTORIQUE FACTURES ----------
    st.divider()
    st.subheader("📂 Historique des analyses de factures")

    if not st.session_state.history_invoice:
        st.info("Aucune facture analysée pour le moment.")
    else:
        for i, item in enumerate(reversed(st.session_state.history_invoice), 1):
            st.markdown(f"### Facture {i} — {item['file_name']}")
            structured = item["structured"]

            if structured:
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**Fournisseur :**", structured.get("vendor", "—"))
                    st.write("**N° facture :**", structured.get("invoice_number", "—"))
                    st.write("**Date :**", structured.get("date", "—"))
                with c2:
                    st.write("**Total HT :**", structured.get("total_ht", "—"))
                    st.write("**TVA :**", structured.get("tva", "—"))
                    st.write("**Total TTC :**", structured.get("total_ttc", "—"))
                    st.write("**Devise :**", structured.get("currency", "—"))

            with st.expander("🔎 Texte OCR (aperçu)"):
                st.code(item.get("raw_text_preview", ""), language="text")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Projet Document Intelligence – CV (RAG) & Factures (OCR) | Streamlit + FastAPI")
