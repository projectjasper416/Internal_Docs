# Internal Docs Q&A Agent - Backend

This is the Flask backend for the Internal Docs Q&A Agent, which provides API endpoints for document indexing and question answering.

## Features

- Google Drive integration for document indexing
- RAG (Retrieval Augmented Generation) pipeline
- Open-source LLM integration (Mistral-7B-Instruct)
- Vector database storage with ChromaDB
- Support for multiple document formats (Google Docs, PDFs, DOCX, etc.)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the environment template and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your configuration:

- `GOOGLE_DRIVE_CREDENTIALS_FILE`: Path to your Google Drive API credentials
- `LLM_MODEL_PATH`: Path to your GGUF model file
- `HF_TOKEN`: Your Hugging Face token (optional)

### 3. Google Drive API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials
5. Download the credentials JSON file
6. Place it in the backend directory as `credentials.json`

### 4. LLM Model Setup

Download a GGUF model file (e.g., Mistral-7B-Instruct) and place it in the `models/` directory:

```bash
mkdir -p models
# Download your preferred GGUF model and place it in models/
```

### 5. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/health`
- Returns server status

### Index Documents
- **POST** `/index_docs`
- Triggers indexing of Google Drive documents
- Returns indexing results

### Ask Question
- **POST** `/ask`
- Request body: `{"question": "Your question here"}`
- Returns answer and source documents

### Chat History
- **GET** `/chat_history`
- Returns chat history (placeholder for future implementation)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── services/
│   │   ├── google_drive_service.py
│   │   ├── rag_service.py
│   │   └── llm_service.py
│   └── utils/
│       └── text_processor.py
├── app.py
├── requirements.txt
├── env.example
└── README.md
```

## Development Notes

- The system uses mock responses when the LLM model is not available
- Google Drive integration requires proper OAuth setup
- Vector database is stored locally in `./chroma_db/`
- Embedding model is downloaded automatically on first use

## Troubleshooting

1. **Model not found**: Ensure the GGUF model file is in the correct location
2. **Google Drive authentication**: Check that `credentials.json` is properly configured
3. **Memory issues**: Reduce `n_threads` in LLMService for lower memory usage
4. **Vector database errors**: Delete `./chroma_db/` directory to reset the database 