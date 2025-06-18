from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag.chain import create_chain
from typing import Dict, Any
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API del Código Nacional de Tránsito",
    description="API para consultar información del código de tránsito usando RAG",
    version="1.0.0"
)

logger.info("[APP] Iniciando aplicación...")

try:
    logger.info("[CHAIN] Iniciando cadena QA con Gemini...")
    qa_chain = create_chain()
    logger.info("[CHAIN] ✅ Cadena QA inicializada correctamente")
except Exception as e:
    logger.error(f"[CHAIN] ⚠️ No se pudo inicializar la cadena QA: {str(e)}")
    qa_chain = None

class Question(BaseModel):
    query: str

class Response(BaseModel):
    response: str
    sources: list[Dict[str, Any]]

@app.post("/ask", response_model=Response)
async def ask_question(question: Question):
    if qa_chain is None:
        raise HTTPException(
            status_code=503,
            detail="Servicio no disponible. Intente más tarde."
        )

    try:
        result = qa_chain.invoke({"query": question.query})

        # Formatear las fuentes para que sean más legibles
        formatted_sources = []
        for doc in result["source_documents"]:
            metadata = doc.metadata
            formatted_sources.append({
                "extracto": doc.page_content.strip().replace("\n", " "),
                "pagina": metadata.get("page_label") or metadata.get("page"),
                "archivo": os.path.basename(metadata.get("source", "desconocido"))
            })

        return {
            "response": result["result"].strip(),
            "sources": formatted_sources
        }

    except Exception as e:
        logger.error(f"Error procesando pregunta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if qa_chain else "degraded",
        "model": "gemini-pro"
    }

@app.get("/")
def root():
    return {
        "message": "API del Código Nacional de Tránsito 🇨🇴",
        "endpoints": {
            "documentación": "/docs",
            "salud": "/health",
            "consultas": "/ask (POST)"
        }
    }
