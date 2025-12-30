from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.chunker import chunk_text
from src.embeddings.embedding_model import load_embedding_model
from src.embeddings.vector_store import build_faiss_index
from src.llm.llm_model import load_llm
from src.llm.prompt import RAG_PROMPT
from src.rag.rag_pipeline import run_rag

# Texte nettoyé (reprends ton résultat)
from src.test.test_clean import cleaned_text

chunks = chunk_text(cleaned_text)

embedding_model = load_embedding_model()
vector_store = build_faiss_index(chunks, embedding_model)

llm = load_llm()

question = "Liste uniquement les compétences explicitement mentionnées"

response = run_rag(
    question=question,
    vector_store=vector_store,
    llm=llm,
    prompt=RAG_PROMPT
)

print("\nRéponse RAG:\n")
print(response)
