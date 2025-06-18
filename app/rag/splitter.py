# app/rag/splitter.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

def split_documents(documents: List[Document]) -> List[Document]:
    """Divide documentos en chunks más pequeños."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    chunks = splitter.split_documents(documents)
    print(f"[SPLITTER] {len(chunks)} chunks generados.")
    return chunks
