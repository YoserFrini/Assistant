from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.ingest import load_documents
from src.chunking import chunk_documents
from src.embeddings import create_vectorstore
from src.retriever import retrieve, build_context, is_out_of_scope
from src.generator import generate_answer

app = FastAPI()



class QuestionRequest(BaseModel):
    question: str



try:
    documents = load_documents()
    chunks = chunk_documents(documents)
    collection = create_vectorstore(chunks)
except Exception as e:
    collection = None
    print(f"Erreur d'initialisation: {e}")


# HEALTH CHECK
@app.get("/health")
def health():
    if collection is None:
        raise HTTPException(
            status_code=500,
            detail="Vector store non initialisé"
        )

    return {
        "status": "ok",
        "documents_loaded": True,
        "nb_documents": len(documents)
    }


# ASK ENDPOINT 
@app.post("/ask")
def ask(request: QuestionRequest):

    question = request.question

    
    if not question or len(question.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Question invalide. Veuillez fournir une question claire."
        )

    try:
        
        docs, metas = retrieve(collection, question)

        
        if is_out_of_scope(docs):
            raise HTTPException(
                status_code=404,
                detail="Aucune information trouvée dans les documents pour cette question."
            )

        
        context = build_context(docs, metas)

        
        answer = generate_answer(question, context)

        
        top_sources = []
        seen = set()

        for m in metas:
            source = m.get("source", "unknown")

            if source not in seen:
                seen.add(source)
                top_sources.append(source)

            if len(top_sources) >= 2:
                break

        
        if len(docs) >= 3:
            confidence = "high"
        elif len(docs) == 2:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "answer": answer,
            "sources": top_sources,
            "confidence": confidence
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne: {str(e)}"
        )