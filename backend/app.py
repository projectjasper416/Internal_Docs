from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from app.services.google_drive_service import GoogleDriveService
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize services
google_drive_service = GoogleDriveService()
rag_service = RAGService()
llm_service = LLMService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Internal Docs Q&A Agent is running"})

@app.route('/index_docs', methods=['POST'])
def index_documents():
    """Index documents from Google Drive"""
    try:
        # Trigger the indexing process
        result = google_drive_service.index_documents()
        rag_service.add_documents(result['documents'])
        return jsonify({
            "status": "success",
            "message": "Documents indexed successfully",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle Q&A requests"""
    try:
        data = request.get_json()
        question = data.get('question')
        if not question:
            return jsonify({
                "status": "error",
                "message": "Question is required"
            }), 400
        
        # Get relevant documents using RAG
        relevant_docs = rag_service.get_relevant_documents(question)
        print("Relevant docs:", relevant_docs)
        # Generate answer using LLM
        answer = llm_service.generate_answer(question, relevant_docs)
        print("Generated answer:", answer)
        
        return jsonify({
            "status": "success",
            "answer": answer,
            "sources": [doc.get('source', 'Unknown') for doc in relevant_docs]
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/chat_history', methods=['GET'])
def get_chat_history():
    """Get chat history (placeholder for future implementation)"""
    return jsonify({
        "status": "success",
        "history": []
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 