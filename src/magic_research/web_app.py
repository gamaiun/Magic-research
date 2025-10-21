"""
Web interface for the RAG Assistant using FastAPI.
Provides a simple frontend for querying the academic documents.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import sys

# Add the parent directory to sys.path for direct execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .models import RAGAssistant
    from .models.model import load_documents
except ImportError:
    # Fallback for direct execution
    from models import RAGAssistant
    from models.model import load_documents

# Initialize FastAPI app
app = FastAPI(title="RAG Assistant", description="Academic Research Assistant")

# Setup templates
template_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_dir)

# Initialize RAG Assistant globally
rag_assistant = None

def initialize_rag():
    """Initialize the RAG assistant with documents."""
    global rag_assistant
    try:
        print("Initializing RAG Assistant for web interface...")
        rag_assistant = RAGAssistant()
        
        # Check if documents exist
        current_count = rag_assistant.get_document_count()
        print(f"Documents in database: {current_count}")
        
        if current_count == 0:
            print("Loading documents...")
            docs = load_documents()
            rag_assistant.add_documents(docs)
            print("✅ Documents loaded successfully")
        else:
            print("✅ Using existing documents in database")
            
    except Exception as e:
        print(f"Error initializing RAG Assistant: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    """Initialize RAG on startup."""
    initialize_rag()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with the query interface."""
    doc_count = rag_assistant.get_document_count() if rag_assistant else 0
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Academic Research Assistant",
        "doc_count": doc_count
    })

@app.post("/query", response_class=HTMLResponse)
async def query(request: Request, question: str = Form(...)):
    """Process user query and return results."""
    if not rag_assistant:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "Academic Research Assistant",
            "error": "RAG Assistant not initialized",
            "question": question,
            "doc_count": 0
        })
    
    try:
        # Process the query
        answer = rag_assistant.invoke(question)
        doc_count = rag_assistant.get_document_count()
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "Academic Research Assistant",
            "question": question,
            "answer": answer,
            "doc_count": doc_count
        })
        
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "Academic Research Assistant",
            "question": question,
            "error": f"Error processing query: {str(e)}",
            "doc_count": rag_assistant.get_document_count()
        })

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "rag_initialized": rag_assistant is not None,
        "document_count": rag_assistant.get_document_count() if rag_assistant else 0
    }

def main():
    """Main entry point for the web application."""
    # Create templates directory if it doesn't exist
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    os.makedirs(template_dir, exist_ok=True)
    
    # Run the FastAPI app
    uvicorn.run(
        "magic_research.web_app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()