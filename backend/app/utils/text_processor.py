import re
from typing import List

class TextProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', '', text)
        
        return text.strip()
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        text = self.clean_text(text)
        
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + self.chunk_size * 0.7:  # Only break if it's not too early
                    end = sentence_end + 1
                else:
                    # Look for paragraph breaks
                    paragraph_end = text.rfind('\n\n', start, end)
                    if paragraph_end > start + self.chunk_size * 0.7:
                        end = paragraph_end + 2
                    else:
                        # Look for word boundary
                        word_end = text.rfind(' ', start, end)
                        if word_end > start + self.chunk_size * 0.7:
                            end = word_end + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break
        
        return chunks
    
    def extract_metadata(self, text: str) -> dict:
        """Extract basic metadata from text"""
        words = text.split()
        sentences = text.split('.')
        
        return {
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'character_count': len(text),
            'has_numbers': bool(re.search(r'\d', text)),
            'has_urls': bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
        }
    
    def is_relevant_chunk(self, chunk: str, min_length: int = 50) -> bool:
        """Check if a chunk is relevant enough to be indexed"""
        if len(chunk.strip()) < min_length:
            return False
        
        # Check if chunk has meaningful content (not just whitespace or special characters)
        meaningful_chars = len(re.sub(r'\s', '', chunk))
        if meaningful_chars < min_length * 0.5:
            return False
        
        return True 