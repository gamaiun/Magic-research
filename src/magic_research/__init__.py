"""
Magic Research: A RAG Assistant for Academic Research

A Retrieval-Augmented Generation (RAG) system designed for semantic search 
and question-answering over academic documents, specifically focused on 
medieval Jewish magic and historical texts.

This package provides:
- PDF document processing and semantic chunking
- Vector-based similarity search using ChromaDB
- Multi-LLM support (OpenAI, Groq, Google Gemini)
- FastAPI web interface for user interaction
- Persistent vector storage for document embeddings

Usage:
    From web interface:
        python -m magic_research.web_app
    
    From command line:
        python -m magic_research.app

Author: Magic Research Contributors
License: CC-BY-NC-SA-4.0
"""

__version__ = "1.0.0"
__author__ = "Magic Research Contributors"
__email__ = "contributors@example.com"
__license__ = "CC-BY-NC-SA-4.0"

# Lazy imports - only import when needed to avoid heavy startup
def get_rag_assistant():
    """Get RAGAssistant class (lazy import)."""
    from .models import RAGAssistant
    return RAGAssistant

def load_documents():
    """Load documents function (lazy import)."""
    from .models.model import load_documents as _load_documents
    return _load_documents()

def get_vector_db():
    """Get VectorDB class (lazy import)."""
    from .data import VectorDB
    return VectorDB

def get_web_app():
    """Get FastAPI app (lazy import)."""
    from .web_app import app
    return app

__all__ = [
    "get_rag_assistant",
    "load_documents", 
    "get_vector_db",
    "get_web_app"
]