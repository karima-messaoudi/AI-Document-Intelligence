def run_rag(question, vector_store, llm, prompt, k=3):
    docs = vector_store.similarity_search(question, k=k)

    if not docs:
        return {
            "answer": "Information non présente dans le CV",
            "sources": []
        }

    context = "\n\n".join(doc.page_content for doc in docs)

    formatted_prompt = prompt.format(
        context=context,
        question=question
    )

    response = llm.invoke(formatted_prompt)

    #  CORRECTION ICI
    if hasattr(response, "content"):
        answer = response.content.strip()
    else:
        answer = str(response).strip()

    #  Nettoyage anti hallucination / prompt replay
    stop_tokens = [
        "[/INST]", "[INST]", "[/USER]",
        "QUESTION :", "RÉPONSE :", "CONTEXTE :"
    ]
    for token in stop_tokens:
        if token in answer:
            answer = answer.split(token)[0].strip()

  

    return {
        "answer": answer,
        "sources": [doc.page_content[:150] for doc in docs]
    }

