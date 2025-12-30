from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

def load_llm():
    load_dotenv()

    hf_token = os.getenv("HF_API_TOKEN")
    if hf_token is None:
        raise ValueError("HF_API_TOKEN manquant")

    llm_endpoint = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        huggingfacehub_api_token=hf_token
    )

    return ChatHuggingFace(llm=llm_endpoint)
