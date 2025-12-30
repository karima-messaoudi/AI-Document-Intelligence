from fastapi import APIRouter, HTTPException
from src.api.schemas import ChatRequest, ChatResponse
from src.api import state
from src.rag.rag_pipeline import run_rag
from src.llm.llm_model import load_llm
from src.llm.prompt import RAG_PROMPT

router = APIRouter(prefix="/chat", tags=["Chat"])

llm = load_llm()

@router.post("", response_model=ChatResponse)
def chat_with_cv(request: ChatRequest):

    if state.vector_store is None:
        raise HTTPException(status_code=400, detail="Aucun CV chargé")

    result = run_rag(
        question=request.question,
        vector_store=state.vector_store,
        llm=llm,
        prompt=RAG_PROMPT
    )

    return result
