"""
Text preprocessing module for preparing documents for RAG processing.
"""

import re
from typing import List, Dict, Any


class TextPreprocessor:
    """
    A text preprocessing class that handles text cleaning, chunking, and preparation
    for vector database storage.
    """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize the text preprocessor.
        
        Args:
            chunk_size: Target size for text chunks (in characters)
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove control characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Normalize line breaks
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Clean up multiple consecutive newlines
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        return text.strip()
    
    def chunk_text(self, text: str, preserve_structure: bool = True) -> List[str]:
        """
        Split text into semantic chunks for better RAG performance.
        
        Args:
            text: Input text to chunk
            preserve_structure: Whether to preserve paragraph and sentence structure
            
        Returns:
            List of text chunks
        """
        chunks = []
        
        if not text or not text.strip():
            return chunks
        
        # Clean the text first
        text = self.clean_text(text)
        
        if preserve_structure:
            # Split by paragraphs to maintain document structure
            paragraphs = text.split('\n\n')
            
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if not paragraph:
                    continue
                
                # If paragraph is small enough, use as-is
                if len(paragraph) <= self.chunk_size:
                    chunks.append(paragraph)
                    continue
                
                # Split large paragraphs by sentences
                chunk_paragraphs = self._chunk_paragraph(paragraph)
                chunks.extend(chunk_paragraphs)
        else:
            # Simple character-based chunking
            chunk_paragraphs = self._chunk_by_size(text)
            chunks.extend(chunk_paragraphs)
        
        # Filter out very small chunks
        chunks = [chunk for chunk in chunks if len(chunk.strip()) > 20]
        
        return chunks
    
    def _chunk_paragraph(self, paragraph: str) -> List[str]:
        """
        Chunk a paragraph by sentences while respecting size limits.
        
        Args:
            paragraph: Paragraph text to chunk
            
        Returns:
            List of paragraph chunks
        """
        # Split paragraph into sentences
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(sentence_pattern, paragraph)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            potential_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            if len(potential_chunk) <= self.chunk_size:
                current_chunk = potential_chunk
            else:
                # Current chunk is full, save it and start new chunk
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # If single sentence is too long, split it further
                if len(sentence) > self.chunk_size:
                    sentence_chunks = self._split_long_sentence(sentence)
                    chunks.extend(sentence_chunks[:-1])  # Add all but last
                    current_chunk = sentence_chunks[-1] if sentence_chunks else ""
                else:
                    current_chunk = sentence
        
        # Add the last chunk if it has content
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_long_sentence(self, sentence: str) -> List[str]:
        """
        Split a very long sentence by commas, semicolons, or other delimiters.
        
        Args:
            sentence: Long sentence to split
            
        Returns:
            List of sentence parts
        """
        # Split by various delimiters
        parts = re.split(r'[,;:]', sentence)
        chunks = []
        current_chunk = ""
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            potential_chunk = current_chunk + ", " + part if current_chunk else part
            
            if len(potential_chunk) <= self.chunk_size:
                current_chunk = potential_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = part
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _chunk_by_size(self, text: str) -> List[str]:
        """
        Simple size-based chunking with overlap.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            
            # If this isn't the last chunk, try to end at a word boundary
            if end < text_length:
                # Look for the last space within the chunk
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start <= 0:
                start = end
        
        return chunks
    
    def create_chunk_metadata(self, chunk: str, chunk_index: int, document_name: str, 
                            total_chunks: int) -> Dict[str, Any]:
        """
        Create metadata for a text chunk.
        
        Args:
            chunk: The text chunk
            chunk_index: Index of this chunk in the document
            document_name: Name of the source document
            total_chunks: Total number of chunks in the document
            
        Returns:
            Dictionary containing chunk metadata
        """
        return {
            "document_name": document_name,
            "chunk_index": chunk_index,
            "chunk_size": len(chunk),
            "total_chunks": total_chunks,
            "preview": chunk[:100] + "..." if len(chunk) > 100 else chunk
        }


def chunk_documents(documents: List[str], chunk_size: int = 500) -> List[Dict[str, Any]]:
    """
    Convenience function to chunk a list of documents.
    
    Args:
        documents: List of document strings
        chunk_size: Target size for chunks
        
    Returns:
        List of dictionaries containing chunks and metadata
    """
    preprocessor = TextPreprocessor(chunk_size=chunk_size)
    all_chunks = []
    
    for doc_idx, document in enumerate(documents):
        # Extract document name from header if available
        doc_name = f"document_{doc_idx}"
        if document.startswith("=== ") and " ===" in document:
            header_end = document.find(" ===\n")
            if header_end > 0:
                doc_name = document[4:header_end].replace(".pdf", "")
        
        # Chunk the document
        chunks = preprocessor.chunk_text(document)
        
        # Create chunk dictionaries with metadata
        for chunk_idx, chunk in enumerate(chunks):
            chunk_data = {
                "text": chunk,
                "metadata": preprocessor.create_chunk_metadata(
                    chunk, chunk_idx, doc_name, len(chunks)
                )
            }
            all_chunks.append(chunk_data)
    
    return all_chunks