from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from app.rag.vectorstore import create_vectorstore
from app.rag.splitter import split_documents
from app.rag.loader import load_documents
import os

def create_chain():
    """Crea y retorna la cadena QA de RAG completa."""
    try:
        documents = load_documents()
        chunks = split_documents(documents)
        vectorstore = create_vectorstore(chunks)

        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY no está configurada en las variables de entorno")
        
        # CORRECCIÓN: Cambiar modelo a gemini-pro
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # ¡Cambiado de gemini-1.0-pro a gemini-pro!
            google_api_key=google_api_key,
            temperature=0.1,
            max_output_tokens=1024
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True
        )

        return qa_chain

    except Exception as e:
        print(f"Error creando cadena QA: {str(e)}")
        raise