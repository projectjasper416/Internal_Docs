# Internal Docs Q&A Agent

An AI-powered internal assistant that indexes team documentation and allows employees to ask natural language questions about company policies, procedures, and internal information.

## 🚀 Features

- **Google Drive Integration**: Index documents from Google Drive (Docs, Sheets, PDFs, DOCX)
- **RAG Pipeline**: Retrieval Augmented Generation for accurate answers
- **Open Source LLM**: Uses Mistral-7B-Instruct for answer generation
- **Modern UI**: Beautiful, responsive React frontend with chat interface
- **Source Attribution**: Shows which documents were used to generate answers
- **Real-time Status**: Connection status indicators and health checks

## 📋 Requirements

### Backend Requirements
- Python 3.9+
- Google Drive API credentials
- GGUF model file (e.g., Mistral-7B-Instruct)
- 4GB+ RAM (for LLM inference)

### Frontend Requirements
- Node.js 16+
- npm or yarn

## 🛠️ Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd internal-docs-qa
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env.example .env

# Edit .env with your configuration
# - Add Google Drive API credentials
# - Set LLM model path
# - Configure other settings

# Create models directory and add your GGUF model
mkdir -p models
# Download your preferred GGUF model and place it in models/
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

### 4. Run the Application

```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Start frontend
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 🔧 Configuration

### Google Drive API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials JSON file
6. Place it in the backend directory as `credentials.json`

### LLM Model Setup

Download a GGUF model file and place it in the `backend/models/` directory:

```bash
# Example: Download Mistral-7B-Instruct
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf -O backend/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Google Drive API Configuration
GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json

# LLM Configuration
LLM_MODEL_PATH=./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf

# Hugging Face Token (optional)
HF_TOKEN=your_huggingface_token_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Vector Database Configuration
CHROMA_DB_PATH=./chroma_db

# Embedding Model Configuration
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

## 📚 API Endpoints

### Health Check
- **GET** `/health` - Check backend status

### Document Indexing
- **POST** `/index_docs` - Index Google Drive documents

### Question Answering
- **POST** `/ask` - Ask a question
  - Body: `{"question": "Your question here"}`
  - Returns: `{"answer": "...", "sources": [...]}`

### Chat History
- **GET** `/chat_history` - Get chat history (placeholder)

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   React App     │ ◄──────────────► │  Flask Backend  │
│   (Frontend)    │                 │   (Python)      │
└─────────────────┘                 └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │   RAG Pipeline  │
                                    │                 │
                                    │ • Google Drive  │
                                    │ • Text Chunking │
                                    │ • Embeddings    │
                                    │ • Vector DB     │
                                    │ • LLM Inference │
                                    └─────────────────┘
```

## 🔍 How It Works

1. **Document Indexing**: 
   - Connects to Google Drive API
   - Downloads and extracts text from documents
   - Chunks text into semantic segments
   - Generates embeddings and stores in ChromaDB

2. **Question Answering**:
   - Converts user question to embedding
   - Performs similarity search in vector database
   - Retrieves relevant document chunks
   - Generates answer using LLM with context

3. **User Interface**:
   - Modern chat interface
   - Real-time status indicators
   - Source attribution
   - Responsive design

## 📁 Project Structure

```
internal-docs-qa/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── google_drive_service.py
│   │   │   ├── rag_service.py
│   │   │   └── llm_service.py
│   │   └── utils/
│   │       └── text_processor.py
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.js
│   │   │   ├── Header.js
│   │   │   └── Message.js
│   │   └── services/
│   │       └── api.js
│   ├── package.json
│   └── README.md
└── README.md
```

## 🚀 Deployment

### Development
```bash
# Backend
cd backend && python app.py

# Frontend
cd frontend && npm start
```

### Production
```bash
# Build frontend
cd frontend && npm run build

# Serve with nginx or similar
# Configure backend as service
```

## 🔧 Troubleshooting

### Common Issues

1. **Backend not connecting**:
   - Check if Flask server is running on port 5000
   - Verify CORS settings
   - Check console for error messages

2. **Google Drive authentication**:
   - Ensure `credentials.json` is properly configured
   - Check OAuth 2.0 setup in Google Cloud Console
   - Verify API permissions

3. **LLM model not loading**:
   - Check model file path in `.env`
   - Ensure sufficient RAM (4GB+)
   - Try smaller model if memory issues

4. **Vector database errors**:
   - Delete `./chroma_db/` directory to reset
   - Check disk space
   - Verify ChromaDB installation

### Performance Tips

- Use smaller GGUF models for faster inference
- Increase `n_threads` for better CPU utilization
- Enable GPU acceleration if available
- Optimize document chunking parameters

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Mistral AI](https://mistral.ai/) for the open-source LLM
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [React](https://reactjs.org/) for the frontend framework
- [Flask](https://flask.palletsprojects.com/) for the backend framework 