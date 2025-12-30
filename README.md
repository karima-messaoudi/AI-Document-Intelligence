# 📄 AI Document Intelligence – CV & Facture Analyzer (RAG + OCR + LLM)

Un projet intelligent d’analyse automatique de documents basé sur **FastAPI + Streamlit + RAG + OCR**.  
Il permet de :

✔ Interroger un **CV en langage naturel** et obtenir des réponses précises  
✔ Extraire les informations clés d’une **facture (image)** grâce à l’OCR  
✔ Afficher les champs structurés + aperçu texte OCR  
✔ Utiliser un **pipeline RAG** avec embeddings & FAISS pour les PDF  
✔ Interface web simple et ergonomique pour l’utilisateur  
<img width="1920" height="926" alt="image" src="https://github.com/user-attachments/assets/3eabbbc4-ab10-42d9-8a72-edb279b43f13" />

<img width="1839" height="930" alt="image" src="https://github.com/user-attachments/assets/c8b51a43-3ba8-4af3-bf62-bb20cdf49664" />



> 🎯 Objectif : automatiser l’analyse documentaire, faciliter la recherche d’information et poser les bases d’un assistant IA évolutif.

## 🚀 Fonctionnalités

### 🔍 Analyse de CV (PDF)
- Extraction du texte
- Découpage en chunks
- Embeddings + Indexation vectorielle (FAISS)
- Questions en langage naturel (ex : *"Dans quelle université le candidat a fait son master ?"*)
- Retour de la réponse + sources

### 🧾 Analyse de Factures (Images)
- OCR via `pytesseract`
- Nettoyage & structuration du texte
- Extraction automatique :(Fournisseur, Numéro facture, Montant HT,  TVA & taux, Devise, ...)
- Interface d’affichage structurée 

### 💻 Interface Streamlit
- Upload CV PDF ou Facture image
- Résultat affiché instantanément
- Historique Q/R pour les CV
- Preview OCR + tableau résumé facture

## 🔧 Installation & Lancement

git clone https://github.com/USERNAME/document-intelligence-rag.git
cd document-intelligence-rag

### 2. Installer les dépendances

Assure-toi d’avoir Python ≥ 3.9

pip install -r requirements.txt

### 3. Installer Tesseract OCR

🔗 Télécharger : https://github.com/UB-Mannheim/tesseract/wiki

Après installation, ajouter dans ocr_loader.py  :

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

### 4. Lancer l'API FastAPI
uvicorn src.api.main:app --reload --port 8000
API disponible sur → http://127.0.0.1:8000
Documentation interactive → http://127.0.0.1:8000/docs

### 5. Lancer l’interface utilisateur (Streamlit)
streamlit run streamlit_app/app.py
Interface accessible sur → http://localhost:850
