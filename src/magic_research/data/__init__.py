"""
Data processing modules for the magic research project.

This package contains modules for loading, processing, and preparing documents
for the RAG (Retrieval-Augmented Generation) system.
"""

from .loader import DocumentLoader, load_pdf_documents
from .preprocessor import TextPreprocessor, chunk_documents
from .vectordb import VectorDB

__all__ = [
    "DocumentLoader",
    "load_pdf_documents", 
    "TextPreprocessor",
    "chunk_documents",
    "VectorDB"
]