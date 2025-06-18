# app/rag/vectorstore.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List
from langchain.schema import Document

def create_vectorstore(docs: List[Document]) -> FAISS:
    """Crea un vectorstore FAISS a partir de documentos usando embeddings de HuggingFace."""
    if not docs:
        raise ValueError("No se proporcionaron documentos para indexar en FAISS.")

    try:
        print("[VECTORSTORE] Generando embeddings con HuggingFace...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)
        print("[VECTORSTORE] Vectorstore FAISS creado correctamente.")
        return vectorstore
    except IndexError:
        raise RuntimeError("No se pudieron generar embeddings. Verifica que los documentos no estén vacíos.")
    except Exception as e:
        raise RuntimeError(f"Error al crear el vectorstore: {str(e)}")