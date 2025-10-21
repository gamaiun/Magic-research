"""
Document loader module for handling PDF files and other document formats.
"""

import os
import glob
from typing import List, Dict, Any
import PyPDF2


class DocumentLoader:
    """
    A document loader class that handles various document formats.
    Currently supports PDF files with plans to extend to other formats.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the document loader.
        
        Args:
            data_dir: Path to the directory containing documents.
                     If None, will use the project's data directory.
        """
        if data_dir is None:
            # Calculate path to project's data directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            magic_research_dir = os.path.dirname(current_dir)  # Go up from data/
            src_dir = os.path.dirname(magic_research_dir)      # Go up from magic_research/
            project_root = os.path.dirname(src_dir)            # Go up from src/
            data_dir = os.path.join(project_root, "data")
        
        self.data_dir = data_dir
        
    def load_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Load a single PDF file and extract its text content.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing document metadata and content
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from all pages
                document_text = ""
                page_count = len(pdf_reader.pages)
                
                for page_num in range(page_count):
                    page = pdf_reader.pages[page_num]
                    document_text += page.extract_text() + "\n"
                
                # Create document metadata
                filename = os.path.basename(pdf_path)
                doc_name = filename.replace(".pdf", "")
                
                return {
                    "filename": filename,
                    "document_name": doc_name,
                    "file_path": pdf_path,
                    "content": document_text.strip(),
                    "page_count": page_count,
                    "char_count": len(document_text),
                    "format": "pdf"
                }
                
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return None
    
    def load_all_pdfs(self) -> List[Dict[str, Any]]:
        """
        Load all PDF files from the data directory.
        
        Returns:
            List of document dictionaries
        """
        pdf_files = glob.glob(os.path.join(self.data_dir, "*.pdf"))
        documents = []
        
        print(f"Found {len(pdf_files)} PDF files in {self.data_dir}")
        
        for pdf_file in pdf_files:
            print(f"Loading: {os.path.basename(pdf_file)}")
            
            doc = self.load_pdf(pdf_file)
            if doc and doc["content"]:
                documents.append(doc)
                print(f"  - Extracted {doc['char_count']} characters from {doc['page_count']} pages")
            else:
                print(f"  - Warning: No text extracted from {pdf_file}")
        
        print(f"Successfully loaded {len(documents)} documents")
        return documents
    
    def format_document(self, doc: Dict[str, Any]) -> str:
        """
        Format a document dictionary into a string suitable for RAG processing.
        
        Args:
            doc: Document dictionary from load_pdf
            
        Returns:
            Formatted document string with header and content
        """
        header = f"=== {doc['filename']} ==="
        return f"{header}\n\n{doc['content']}"


def load_pdf_documents(data_dir: str = None) -> List[str]:
    """
    Convenience function to load all PDF documents as formatted strings.
    
    Args:
        data_dir: Path to directory containing PDF files
        
    Returns:
        List of formatted document strings ready for RAG processing
    """
    loader = DocumentLoader(data_dir)
    documents = loader.load_all_pdfs()
    
    return [loader.format_document(doc) for doc in documents]