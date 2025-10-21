"""
Web interface for the RAG Assistant using FastAPI.
Provides a simple frontend for querying the academic documents.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
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

# Global variable for RAG Assistant
rag_assistant = None

def initialize_rag():
    """Initialize the RAG assistant with documents."""
    global rag_assistant
    try:
        print("🚀 Initializing RAG Assistant for web interface...")
        rag_assistant = RAGAssistant()
        
        # Check if documents exist
        current_count = rag_assistant.get_document_count()
        print(f"📊 Documents in database: {current_count}")
        
        if current_count == 0:
            print("📚 Loading documents...")
            docs = load_documents()
            rag_assistant.add_documents(docs)
            print("✅ Documents loaded successfully")
        else:
            print("✅ Using existing documents in database")
            
        print("🎉 RAG Assistant initialization complete!")
        return True
            
    except Exception as e:
        print(f"❌ Error initializing RAG Assistant: {e}")
        import traceback
        traceback.print_exc()
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    # Startup - backend is already initialized in main()
    print("🎉 Web server ready to accept requests!")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down RAG Assistant Web Interface...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="RAG Assistant", 
    description="Academic Research Assistant",
    lifespan=lifespan
)

# Setup templates
template_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_dir)

@app.get("/health")
async def health_check():
    """Health check endpoint to verify backend readiness."""
    if not rag_assistant:
        return {"status": "error", "message": "RAG Assistant not initialized"}
    
    try:
        doc_count = rag_assistant.get_document_count()
        return {
            "status": "ready", 
            "message": "RAG Assistant is ready",
            "document_count": doc_count
        }
    except Exception as e:
        return {"status": "error", "message": f"Backend error: {str(e)}"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with the query interface."""
    # Check backend readiness
    backend_status = "ready" if rag_assistant else "not_ready"
    doc_count = 0
    error_message = None
    
    if rag_assistant:
        try:
            doc_count = rag_assistant.get_document_count()
        except Exception as e:
            backend_status = "error"
            error_message = f"Backend error: {str(e)}"
    else:
        error_message = "RAG Assistant is initializing... Please wait and refresh the page."
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Magic Research",
        "doc_count": doc_count,
        "backend_status": backend_status,
        "error": error_message if backend_status != "ready" else None
    })

@app.post("/query", response_class=HTMLResponse)
async def query(request: Request, question: str = Form(...)):
    """Process user query and return results."""
    # Check if backend is ready
    if not rag_assistant:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "Magic Research",
            "error": "🔧 RAG Assistant is still initializing. Please wait a moment and try again.",
            "question": question,
            "doc_count": 0,
            "backend_status": "not_ready"
        })
    
    try:
        # Verify backend is working
        doc_count = rag_assistant.get_document_count()
        if doc_count == 0:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "title": "Magic Research",
                "error": "📚 No documents loaded in the database. Please check the backend initialization.",
                "question": question,
                "doc_count": 0,
                "backend_status": "no_documents"
            })
        
        # Process the query
        print(f"🔍 Processing query: '{question}'")
        answer = rag_assistant.invoke(question)
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "Magic Research",
            "question": question,
            "answer": answer,
            "doc_count": doc_count,
            "backend_status": "ready"
        })
        
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        import traceback
        traceback.print_exc()
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "title": "Magic Research",
            "question": question,
            "error": f"🚨 Error processing your query: {str(e)}",
            "doc_count": rag_assistant.get_document_count() if rag_assistant else 0,
            "backend_status": "error"
        })

def main():
    """Main entry point for the web application."""
    print("🚀 Starting Magic Research RAG Assistant...")
    
    # Create templates directory if it doesn't exist
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    os.makedirs(template_dir, exist_ok=True)
    
    # Initialize backend BEFORE starting Uvicorn
    print("🔧 Initializing backend systems...")
    success = initialize_rag()
    
    if not success:
        print("💥 CRITICAL: Backend initialization failed!")
        print("🛑 Cannot start web server without working backend.")
        print("📋 Please check:")
        print("   - Virtual environment is activated")
        print("   - All dependencies are installed")
        print("   - Database path is accessible")
        print("   - PDF documents are in data/ directory")
        return
    
    print("✅ Backend initialization complete!")
    print("🌐 Starting web server...")
    
    # Now start Uvicorn - backend is ready
    uvicorn.run(
        app,  # Use the app object directly instead of string import
        host="127.0.0.1",
        port=8001,  # Changed to 8001 to avoid port conflicts
        reload=False,  # Disable reload to prevent lifespan conflicts
        log_level="info"
    )

if __name__ == "__main__":
    main()