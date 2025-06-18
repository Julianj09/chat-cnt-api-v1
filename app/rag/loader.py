from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document
from typing import List
import os
import glob

def load_documents(path: str = "app/rag/data") -> List[Document]:
    """Carga documentos de texto (.txt) y PDF (.pdf) desde un directorio."""
    try:
        print(f"[Loader] Buscando documentos en: {os.path.abspath(path)}")
        documents: List[Document] = []

        # Cargar archivos .txt
        txt_files = glob.glob(os.path.join(path, "**/*.txt"), recursive=True)
        for file_path in txt_files:
            loader = TextLoader(file_path, autodetect_encoding=True)
            documents.extend(loader.load())

        # Cargar archivos .pdf
        pdf_files = glob.glob(os.path.join(path, "**/*.pdf"), recursive=True)
        for file_path in pdf_files:
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())

        print(f"[Loader] Documentos cargados: {len(documents)}")

        if not documents:
            print("[Loader] ⚠️ No se encontraron documentos válidos en el directorio.")

        return documents

    except Exception as e:
        raise RuntimeError(f"[Loader] Error cargando documentos: {str(e)}")