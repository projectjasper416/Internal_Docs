# Internal Docs Q&A Agent - Backend

This is the Flask backend for the Internal Docs Q&A Agent, which provides API endpoints for document indexing and question answering.

## Features

- Google Drive integration for document indexing
- RAG (Retrieval Augmented Generation) pipeline
- Gemini API integration for answer generation
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
- `GEMINI_API_KEY`: Your Google AI Studio API key
- `GEMINI_MODEL`: Gemini model name (default: `gemini-1.5-flash`)
- `HF_TOKEN`: Your Hugging Face token (optional)

### 3. Google Drive API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials
5. Download the credentials JSON file
6. Place it in the backend directory as `credentials.json`

### 4. Gemini API Setup

Create a Gemini API key in Google AI Studio and set it in `.env`:

```bash
# Example
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
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

- The system uses mock responses when Gemini configuration is not available
- Google Drive integration requires proper OAuth setup
- Vector database is stored locally in `./chroma_db/`
- Embedding model is downloaded automatically on first use

## Troubleshooting

1. **Gemini not configured**: Ensure `GEMINI_API_KEY` is set in `.env`
2. **Google Drive authentication**: Check that `credentials.json` is properly configured
3. **API errors**: Verify your Gemini key and model name are valid
4. **Vector database errors**: Delete `./chroma_db/` directory to reset the database 