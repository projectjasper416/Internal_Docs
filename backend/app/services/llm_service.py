import os
from typing import List, Dict, Any
from llama_cpp import Llama
import json

class LLMService:
    def __init__(self):
        self.model_path = os.getenv('LLM_MODEL_PATH', './models/mistral-7b-instruct-v0.2.Q4_K_M.gguf')
        self.llm = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the LLM model"""
        try:
            if os.path.exists(self.model_path):
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=4096,  # Context window
                    n_threads=4,  # Number of CPU threads
                    n_gpu_layers=0  # Set to > 0 if GPU is available
                )
                print(f"LLM model loaded successfully from {self.model_path}")
            else:
                print(f"Warning: Model file not found at {self.model_path}")
                print("Using mock responses for development")
                self.llm = None
        except Exception as e:
            print(f"Error loading LLM model: {e}")
            print("Using mock responses for development")
            self.llm = None
    
    def _create_prompt(self, question: str, context_docs: List[Dict[str, Any]]) -> str:
        """Create a prompt for the LLM"""
        context_text = ""
        sources = []
        
        for i, doc in enumerate(context_docs, 1):
            context_text += f"Document {i} ({doc.get('source', 'Unknown')}):\n{doc.get('content', '')}\n\n"
            sources.append(doc.get('source', 'Unknown'))
        
        prompt = f"""You are a helpful assistant that answers questions based on internal company documentation. 
Use only the information provided in the context below to answer the question. 
If the information is not available in the context, say "I don't have enough information to answer this question."

Context:
{context_text}

Question: {question}

Answer:"""
        
        return prompt
    
    def generate_answer(self, question: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generate an answer using the LLM"""
        if not context_docs:
            return "I don't have enough information to answer this question. Please try rephrasing your query or contact your administrator to ensure relevant documents are indexed."
        
        try:
            if self.llm:
                # Use the actual LLM
                prompt = self._create_prompt(question, context_docs)
                
                response = self.llm(
                    prompt,
                    max_tokens=512,
                    temperature=0.1,
                    stop=["Question:", "\n\n"]
                )
                
                answer = response['choices'][0]['text'].strip()
                return answer
            else:
                # Mock response for development
                return self._generate_mock_answer(question, context_docs)
                
        except Exception as e:
            print(f"Error generating answer: {e}")
            return f"I encountered an error while processing your question. Please try again or contact support. Error: {str(e)}"
    
    def _generate_mock_answer(self, question: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generate a mock answer for development purposes"""
        sources = [doc.get('source', 'Unknown') for doc in context_docs]
        
        # Simple keyword-based mock responses
        question_lower = question.lower()
        
        if 'policy' in question_lower or 'procedure' in question_lower:
            return f"Based on the available documentation, here's what I found about policies and procedures. The information comes from: {', '.join(sources[:2])}."
        
        elif 'expense' in question_lower or 'report' in question_lower:
            return f"For expense reporting, please refer to the company's expense policy document. The relevant information can be found in: {', '.join(sources[:2])}."
        
        elif 'benefit' in question_lower or 'hr' in question_lower:
            return f"Regarding benefits and HR policies, please check the HR documentation. Sources: {', '.join(sources[:2])}."
        
        elif 'technical' in question_lower or 'api' in question_lower or 'documentation' in question_lower:
            return f"For technical documentation and API information, please refer to the technical docs. Sources: {', '.join(sources[:2])}."
        
        else:
            return f"I found some relevant information in the company documentation. Please refer to: {', '.join(sources[:2])} for more details."
    
    def validate_question(self, question: str) -> Dict[str, Any]:
        """Validate if a question is appropriate for the system"""
        if not question or len(question.strip()) < 3:
            return {
                'valid': False,
                'reason': 'Question is too short. Please provide more details.'
            }
        
        if len(question) > 500:
            return {
                'valid': False,
                'reason': 'Question is too long. Please keep it under 500 characters.'
            }
        
        # Check for inappropriate content (basic filter)
        inappropriate_keywords = ['password', 'credit card', 'ssn', 'social security']
        question_lower = question.lower()
        
        for keyword in inappropriate_keywords:
            if keyword in question_lower:
                return {
                    'valid': False,
                    'reason': 'This type of question is not appropriate for this system.'
                }
        
        return {'valid': True}
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if self.llm:
            return {
                'model_loaded': True,
                'model_path': self.model_path,
                'context_window': 4096,
                'model_type': 'Mistral-7B-Instruct'
            }
        else:
            return {
                'model_loaded': False,
                'model_path': self.model_path,
                'note': 'Using mock responses for development'
            } 