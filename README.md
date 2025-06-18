# 📚 ChatBot del Código Nacional de Tránsito (Colombia)

Un sistema de preguntas y respuestas basado en IA que utiliza **RAG** (Retrieval-Augmented Generation) para proporcionar información precisa del Código Nacional de Tránsito Colombiano.

---

## 🌟 Características principales

- **Tecnología RAG**: Combina recuperación de información con generación de respuestas.
- **Modelo Gemini 2.0 Flash**: Potenciado por IA de Google.
- **Procesamiento de documentos**: Soporte para archivos PDF y texto.
- **API RESTful**: Interfaz fácil de integrar con otros sistemas.
- **Sistema de referencias**: Muestra las fuentes de información utilizadas.

---

## 🛠️ Requisitos técnicos

- Python 3.10+ (Actual: `Python 3.13.3`)
- Node.js 18+ (Actual: `v22.15.1`)
- Vue CLI (Actual: `@vue/cli 5.0.8`)
- Cuenta de Google Cloud con API Key para Gemini AI
- Espacio en disco para almacenar los documentos del código de tránsito

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/chat-cnt-api.git
cd chat-cnt-api
```

### 2. Configurar entorno virtual (Python)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
GOOGLE_API_KEY=tu_api_key_de_google
```

### 5. Preparar documentos

Colocar los archivos PDF y TXT del código de tránsito en:

```
app/rag/data/
```

---

## 🏃 Ejecución del proyecto

Iniciar el servidor FastAPI:

```bash
uvicorn main:app --reload
```

La API estará disponible en:

- Interfaz Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- Endpoint principal: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📝 Uso de la API

### Realizar una consulta

**POST** `/ask`

```json
{
  "query": "¿Cuál es la multa por exceso de velocidad?"
}
```

### Respuesta de ejemplo

```json
{
  "response": "El exceso de velocidad está sancionado con multa tipo 4 según el artículo 131 del CNT...",
  "sources": [
    {
      "extracto": "Artículo 131. Exceso de velocidad. Multa tipo 4...",
      "pagina": 45,
      "archivo": "codigo_transito.pdf"
    }
  ]
}
```

---

## 🧰 Estructura del proyecto

```
chat-cnt-api/
├── app/
│   ├── rag/
│   │   ├── chain.py          # Cadena QA principal
│   │   ├── loader.py         # Carga de documentos
│   │   ├── splitter.py       # División de textos
│   │   ├── vectorstore.py    # Almacenamiento vectorial
│   │   └── data/             # Documentos del código
|   |---main.py                   # Aplicación FastAPI
├── requirements.txt          # Dependencias Python
└── .env                      # Variables de entorno
```
