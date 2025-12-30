from langchain_community.vectorstores import FAISS

def build_faiss_index(texts, embedding_model):
    return FAISS.from_texts(texts, embedding_model)
