# Data Directory

This directory contains the academic documents used by the Magic Research RAG Assistant system.

## Data Sources

The PDF documents in this directory were acquired from [Academia.edu](https://www.academia.edu/), a platform for sharing academic research.

### Current Documents

1. **Abraham_of_Worms_the_disciple_of_Abramel (1).pdf**

   - Primary source document about Abraham of Worms
   - Medieval Jewish magical texts and practices
   - 10 pages, ~37,373 characters

2. **Enchanting_Rabbis_Contest_Narratives_bet (3).pdf**

   - Academic analysis of rabbinic magical contest narratives
   - 42 pages, ~113,520 characters

3. **Gideon_Bohak_Jewish_Magic_in_the_Middle (2).pdf**
   - Scholarly work on Jewish magic in the Middle Ages
   - 33 pages, ~97,160 characters

## Data Acquisition Instructions

### From Academia.edu

1. **Search for relevant papers**:

   - Visit [https://www.academia.edu/](https://www.academia.edu/)
   - Search for terms like: "Abraham of Worms", "Jewish magic", "medieval magic", "Sefer Raziel"
   - Use advanced search filters for academic disciplines: Religious Studies, Jewish Studies, Medieval Studies

2. **Download papers**:

   - Look for papers with PDF download options
   - Some papers may require free registration
   - Respect copyright and fair use guidelines
   - Focus on academic publications and scholarly articles

3. **Recommended search terms**:
   - "Abraham of Worms"
   - "Jewish magical texts"
   - "Medieval Jewish magic"
   - "Sefer Raziel ha-Malakh"
   - "Jewish mysticism medieval"
   - "Practical Kabbalah"
   - "Jewish magical practices"

### Data Processing

Once PDFs are added to this directory:

1. **Automatic Processing**: The system will automatically detect and process new PDF files
2. **Text Extraction**: Content is extracted using PyPDF2
3. **Chunking**: Documents are split into semantic chunks (~500 characters)
4. **Vectorization**: Text chunks are converted to embeddings using sentence-transformers
5. **Storage**: Embeddings are stored in ChromaDB for semantic search

### Adding New Documents

To add new documents to the system:

1. **Place PDF files** in this `data/` directory
2. **Run the reload script**: `python reload_pdfs.py` from the project root
3. **Verify processing**: Check the terminal output for successful document processing

### File Naming Conventions

- Use descriptive filenames that indicate the content
- Include author names or key identifying information
- Use underscores instead of spaces
- Keep the `.pdf` extension

### Quality Guidelines

For best results, ensure PDFs:

- ✅ Are text-based (not scanned images)
- ✅ Have clear, readable text
- ✅ Are academic or scholarly sources
- ✅ Are relevant to medieval Jewish magic and mysticism
- ✅ Are properly formatted and not corrupted

### Copyright and Ethics

- Only use documents that are freely available or properly licensed
- Respect copyright laws and fair use guidelines
- Give proper attribution to original authors
- Use for educational and research purposes only
- Consider reaching out to authors for permission when appropriate

### Current Status

**Total Documents**: 3 PDFs  
**Total Text Chunks**: ~641 semantic chunks  
**Vector Database**: ChromaDB with sentence-transformers embeddings  
**Search Capability**: Semantic similarity search enabled

## Technical Details

- **Text Processing**: PyPDF2 for extraction, custom semantic chunking
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` model
- **Vector Store**: ChromaDB persistent storage
- **Chunk Size**: ~500 characters with semantic boundaries
- **Search**: Cosine similarity with configurable result count
