import os
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any
import json

class RAGService:
    def __init__(self):
        self.embedding_model = SentenceTransformer('BAAI/bge-small-en-v1.5')
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection_name = "internal_docs"
        self.collection = None
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize or get the ChromaDB collection"""
        try:
            self.collection = self.chroma_client.get_collection(self.collection_name)
        except:
            # Create new collection if it doesn't exist
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector database"""
        if not documents:
            return
        
        # Prepare data for ChromaDB
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            ids.append(doc['id'])
            texts.append(doc['content'])
            metadatas.append({
                'source': doc['source'],
                'file_id': doc['file_id'],
                'mime_type': doc['mime_type'],
                'modified_time': doc['modified_time']
            })
        
        # Add to collection
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Added {len(documents)} documents to vector database")
    
    def get_relevant_documents(self, query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query"""
        try:
            # Query the collection
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            print(results)
            # Format results
            documents = []
            if results['documents'] and results['documents'][0]:
                print("Ok")
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'content': doc,
                        'source': results['metadatas'][0][i]['source'],
                        'file_id': results['metadatas'][0][i]['file_id'],
                        'mime_type': results['metadatas'][0][i]['mime_type'],
                        'modified_time': results['metadatas'][0][i]['modified_time'],
                        'similarity_score': results['distances'][0][i] if 'distances' in results else None
                    })
            
            return documents
            
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
    
    def update_documents(self, documents: List[Dict[str, Any]]):
        """Update existing documents in the vector database"""
        if not documents:
            return
        
        # Delete existing documents with same IDs
        ids_to_update = [doc['id'] for doc in documents]
        try:
            self.collection.delete(ids=ids_to_update)
        except:
            pass  # Documents might not exist
        
        # Add updated documents
        self.add_documents(documents)
    
    def delete_documents(self, document_ids: List[str]):
        """Delete documents from the vector database"""
        try:
            self.collection.delete(ids=document_ids)
            print(f"Deleted {len(document_ids)} documents from vector database")
        except Exception as e:
            print(f"Error deleting documents: {e}")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': self.collection_name
            }
        except Exception as e:
            print(f"Error getting collection stats: {e}")
            return {'total_documents': 0, 'collection_name': self.collection_name}
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            self.chroma_client.delete_collection(self.collection_name)
            self._initialize_collection()
            print("Collection cleared successfully")
        except Exception as e:
            print(f"Error clearing collection: {e}")
    
    def search_similar(self, text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar documents to a given text"""
        return self.get_relevant_documents(text, top_k) 