from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag.chain import create_chain
from typing import List, Optional
import os
import logging
from dotenv import load_dotenv

# Configuración inicial
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API del Código Nacional de Tránsito",
    description="API para consultar información del código de tránsito usando RAG + Gemini",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar para producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar cadena QA y modelo LLM
qa_chain = None
llm_model = None

try:
    logger.info("[CHAIN] Iniciando cadena QA con Gemini...")
    qa_chain, llm_model = create_chain()
    logger.info("[CHAIN] ✅ Cadena QA inicializada correctamente")
except Exception as e:
    logger.error(f"[CHAIN] ⚠️ No se pudo inicializar la cadena QA: {str(e)}")

# Modelos
class Question(BaseModel):
    query: str

class SourceDocument(BaseModel):
    extracto: str
    pagina: Optional[str] = None
    archivo: str

class Response(BaseModel):
    response: str
    sources: List[SourceDocument]
    context_used: bool

@app.post("/ask", response_model=Response)
async def ask_question(question: Question):
    if qa_chain is None or llm_model is None:
        raise HTTPException(status_code=503, detail="Servicio no disponible. Intente más tarde.")

    try:
        logger.info(f"[ASK] Procesando pregunta: {question.query[:100]}...")

        # 1. Ejecutar RAG
        result = qa_chain.invoke({"query": question.query})
        source_docs = result.get("source_documents", [])
        has_sources = len(source_docs) > 0

        # 2. Preparar contexto
        formatted_sources = []
        context_texts = []
        for doc in source_docs:
            metadata = doc.metadata
            extracto = doc.page_content.strip().replace("\n", " ")
            context_texts.append(extracto)
            formatted_sources.append({
                "extracto": extracto[:300] + "...",
                "pagina": metadata.get("page_label") or metadata.get("page") or None,
                "archivo": os.path.basename(metadata.get("source", "documento_desconocido"))
            })

        # 3. Armar prompt híbrido
        joined_context = "\n\n".join(f"- {ctx}" for ctx in context_texts) if has_sources else "Sin contexto legal relevante."

        hybrid_prompt = f"""
Eres un experto en tránsito colombiano. El usuario te hace la siguiente pregunta:

\"{question.query}\"

Te proporciono algunos fragmentos legales que podrían estar relacionados:

{joined_context}

Si alguno de los fragmentos contiene una respuesta directa o relacionada con la pregunta, úsala exactamente. 
Si no hay información útil en los fragmentos, responde usando tu conocimiento general.

Responde de forma clara, breve y útil, en máximo 6 líneas.
Evita explicaciones largas o técnicas innecesarias.

Respuesta:
"""

        logger.info("[PROMPT] Enviando prompt híbrido a Gemini...")
        response_text = llm_model.invoke(hybrid_prompt).content.strip()

        return {
            "response": response_text,
            "sources": formatted_sources,
            "context_used": has_sources
        }

    except Exception as e:
        logger.error(f"❌ Error procesando pregunta: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al procesar tu pregunta. Por favor intenta nuevamente."
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if qa_chain and llm_model else "degraded",
        "model": "gemini-2.0-flash",
        "ready": qa_chain is not None
    }

@app.get("/")
def root():
    return {
        "message": "API del Código Nacional de Tránsito Colombiano 🇨🇴",
        "endpoints": {
            "documentación": "/docs",
            "salud": "/health",
            "consultas": "/ask (POST)"
        },
        "version": app.version
    }
