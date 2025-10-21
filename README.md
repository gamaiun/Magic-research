# RAG Assistant for Academic Research

A Retrieval-Augmented Generation (RAG) system designed for semantic search and question-answering over academic documents, specifically focused on medieval Jewish magic and historical texts.

## Overview

This project implements a complete RAG pipeline that processes PDF documents, creates semantic embeddings, stores them in a vector database, and provides an intelligent question-answering interface. The system combines document retrieval with large language model generation to provide contextually accurate answers based on your document corpus.

Key features:

- **PDF Document Processing**: Automatic extraction and chunking of academic papers
- **Semantic Search**: Vector-based similarity search using sentence transformers
- **Multi-LLM Support**: Compatible with OpenAI GPT, Groq Llama, and Google Gemini
- **Web Interface**: User-friendly FastAPI-based frontend
- **Persistent Storage**: ChromaDB vector database for efficient document retrieval

## Target Audience

This project is intended for:

- **Academic Researchers** studying historical texts and manuscripts
- **Digital Humanities Scholars** working with large document collections
- **Graduate Students** conducting literature reviews and research
- **Developers** interested in implementing RAG systems for domain-specific applications

## Prerequisites

### Required Knowledge

- Basic Python programming
- Understanding of virtual environments
- Familiarity with command line interfaces
- Basic knowledge of machine learning concepts (helpful but not required)

### Hardware Requirements

- **RAM**: Minimum 8GB (16GB recommended for larger document collections)
- **Storage**: At least 5GB free space for models and embeddings
- **CPU**: Multi-core processor recommended for faster embedding generation

### System Compatibility

- **Operating Systems**: Windows 10/11, macOS, Linux
- **Python**: Version 3.11 or higher
- **Internet Connection**: Required for initial model downloads and API access

## Installation

### 1. Clone or Download the Project

```bash
cd "path/to/your/projects"
# If using git:
git clone <repository-url>
# Or extract from zip file
```

### 2. Navigate to Project Directory

```bash
cd Project1AiCourse
```

### 3. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Note: On Windows, `uvloop` is automatically excluded from installation as it's not compatible.

## Environment Setup

### 1. Configure API Keys

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` file with your preferred LLM provider:

**Option A: Using Groq (Free tier available)**

```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

**Option B: Using OpenAI**

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

**Option C: Using Google Gemini**

```bash
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-pro
```

### 2. Verify Installation

```bash
# Activate virtual environment
source venv/Scripts/activate  # Windows
# source venv/bin/activate     # macOS/Linux

# Test import
python -c "import chromadb, sentence_transformers, fastapi; print('✅ All dependencies installed successfully')"
```

## Usage

### Quick Start

1. **Start the Web Application**

```bash
# From project root directory
cd src
python web_app.py
```

2. **Access the Interface**
   Open your web browser and navigate to: `http://127.0.0.1:8000`

3. **Ask Questions**
   Try example queries like:

- "What is Abraham of Worms known for?"
- "Describe the magical practices mentioned in the texts"
- "What are the main themes in medieval Jewish magic?"

### Command Line Usage

For direct interaction with the RAG system:

```bash
cd src
python app.py
```

This allows you to:

- Load and process new documents
- Test queries directly in the terminal
- Debug and examine the retrieval process

### Adding New Documents

1. Place PDF files in the `data/` directory
2. The system will automatically detect and process them on startup
3. Documents are chunked semantically and embedded for search

## Data Requirements

### Supported Formats

- **PDF Files**: Academic papers, research documents, manuscripts
- **Text Encoding**: UTF-8 recommended
- **Language**: Optimized for English academic texts

### Document Structure

For best results, documents should have:

- Clear paragraph structure
- Academic or scholarly writing style
- Consistent formatting
- Readable text (not scanned images without OCR)

### Current Dataset

The system includes sample academic papers on:

- Medieval Jewish magic traditions
- Historical manuscript analysis
- Comparative religious studies

## Testing

### Manual Testing

1. Start the web application
2. Navigate to the health check endpoint: `http://127.0.0.1:8000/health`
3. Expected response:

```json
{
  "status": "healthy",
  "rag_initialized": true,
  "document_count": 641
}
```

### Query Testing

Test with known content to verify retrieval:

```bash
# Example test queries
curl -X POST "http://127.0.0.1:8000/query" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "question=Abraham of Worms"
```

## Configuration

### Vector Database Settings

- **Collection Name**: `rag_documents` (configurable in `.env`)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Chunk Size**: 500 characters with semantic boundary detection
- **Database Path**: `./chroma_db/` (persistent storage)

### LLM Configuration

The system supports multiple providers with fallback options:

1. **Primary**: Groq (fast, free tier available)
2. **Secondary**: OpenAI (high quality, paid)
3. **Tertiary**: Google Gemini (alternative option)

### Performance Tuning

- **Chunk Size**: Adjust in `vectordb.py` for different document types
- **Retrieval Count**: Modify `n_results` parameter for more/fewer context chunks
- **Model Selection**: Choose embedding models based on domain specificity

## Methodology

### Document Processing Pipeline

1. **PDF Extraction**: PyPDF2 extracts text content
2. **Semantic Chunking**: Text is split at sentence boundaries while respecting semantic coherence
3. **Embedding Generation**: Sentence transformers create dense vector representations
4. **Vector Storage**: ChromaDB stores embeddings with metadata for efficient retrieval

### Retrieval Process

1. **Query Encoding**: User questions are embedded using the same model
2. **Similarity Search**: Cosine similarity identifies relevant document chunks
3. **Context Assembly**: Top-k results are combined into coherent context
4. **LLM Generation**: Language model generates answers based on retrieved context

### RAG Architecture

```
User Query → Embedding → Vector Search → Context Retrieval → LLM → Response
     ↑                                        ↓
Document → Chunking → Embedding → Vector DB Storage
```

## Performance

### Benchmarks

- **Document Processing**: ~100-200 pages per minute (depending on complexity)
- **Query Response Time**: 2-5 seconds for typical academic questions
- **Memory Usage**: ~2-4GB RAM for moderate document collections (500-1000 pages)
- **Storage Requirements**: ~10-50MB per 100 pages of documents

### Optimization Recommendations

- **Hardware**: SSD storage for faster database access
- **Scaling**: Consider GPU acceleration for large document collections
- **Network**: Stable internet connection for LLM API calls

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions to improve the RAG Assistant! Please follow these guidelines:

1. **Fork the Repository**
2. **Create a Feature Branch**: `git checkout -b feature/new-feature`
3. **Make Changes**: Implement your improvements
4. **Test Thoroughly**: Ensure all functionality works
5. **Submit Pull Request**: Describe your changes clearly

### Areas for Contribution

- Additional document format support (DOCX, TXT, etc.)
- Advanced chunking strategies
- Multi-language support
- Performance optimizations
- UI/UX improvements

## Changelog

### Version 1.0.0 (Current)

- ✅ Initial RAG implementation
- ✅ PDF document processing
- ✅ ChromaDB vector storage
- ✅ Multi-LLM provider support
- ✅ FastAPI web interface
- ✅ Semantic text chunking
- ✅ Persistent embeddings storage

### Planned Features

- [ ] Document upload via web interface
- [ ] Advanced search filters
- [ ] Export functionality for results
- [ ] Multi-language document support
- [ ] Integration with academic databases

## Citation

If you use this RAG Assistant in your academic work, please cite:

```bibtex
@software{rag_assistant_2025,
  title={RAG Assistant for Academic Research},
  author={[Your Name]},
  year={2025},
  url={[Repository URL]},
  note={A Retrieval-Augmented Generation system for academic document analysis}
}
```

## Contact

### Maintainers

- **Primary Developer**: [Your Name]
- **Email**: [your.email@example.com]
- **GitHub**: [Your GitHub Profile]

### Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and community support
- **Documentation**: Check this README and inline code comments

### Academic Collaboration

For academic collaborations or research partnerships, please reach out via email with:

- Brief description of your research project
- Specific use case or requirements
- Timeline and scope of collaboration

---

**Last Updated**: October 2025  
**Project Status**: Active Development  
**Compatibility**: Python 3.11+, Windows/macOS/Linux
