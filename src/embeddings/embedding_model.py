from langchain_huggingface import HuggingFaceEndpointEmbeddings
from dotenv import load_dotenv
import os

def load_embedding_model():
    load_dotenv()

    hf_token = os.getenv("HF_API_TOKEN")
    if hf_token is None:
        raise ValueError("HF_API_TOKEN non trouvé. Vérifie ton fichier .env")

    return HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=hf_token
    )
