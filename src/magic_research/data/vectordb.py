import os
import chromadb
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

try:
    from .preprocessor import chunk_documents
except ImportError:
    # Fallback for direct execution
    from preprocessor import chunk_documents

class VectorDB:
    """
    A simple vector database wrapper using ChromaDB with HuggingFace embeddings.
    """

    def __init__(self, collection_name: str = None, embedding_model: str = None):
        """
        Initialize the vector database.

        Args:
            collection_name: Name of the ChromaDB collection
            embedding_model: HuggingFace model name for embeddings
        """
        self.collection_name = collection_name or os.getenv(
            "CHROMA_COLLECTION_NAME", "rag_documents"
        )
        self.embedding_model_name = embedding_model or os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )

        # Initialize ChromaDB client
        # Use the root project directory for the database
        script_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(script_dir)  # Go up one level from magic_research/
        project_root = os.path.dirname(src_dir)  # Go up another level from src/
        chroma_path = os.path.join(project_root, "chroma_db")
        self.client = chromadb.PersistentClient(path=chroma_path)

        # Load embedding model
        print(f"Loading embedding model: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "RAG document collection"},
        )

        print(f"Vector database initialized with collection: {self.collection_name}")

    def add_documents(self, documents: List[str]) -> None:
        """
        Add documents to the vector database using the new data processing modules.

        Args:
            documents: List of document strings (from PDF loading)
        """
        print(f"Processing {len(documents)} documents...")
        
        # Use the new data processing modules to chunk documents
        chunk_data_list = chunk_documents(documents, chunk_size=500)
        
        if not chunk_data_list:
            print("No chunks to add!")
            return
        
        print(f"Created {len(chunk_data_list)} chunks total")
        
        # Extract data for ChromaDB
        all_chunks = []
        all_ids = []
        all_metadatas = []
        
        for i, chunk_data in enumerate(chunk_data_list):
            chunk_text = chunk_data["text"]
            metadata = chunk_data["metadata"]
            
            # Create unique ID for this chunk
            doc_name = metadata["document_name"]
            chunk_idx = metadata["chunk_index"]
            chunk_id = f"{doc_name}_chunk_{chunk_idx}"
            
            all_chunks.append(chunk_text)
            all_ids.append(chunk_id)
            all_metadatas.append(metadata)
        
        print(f"Creating embeddings for {len(all_chunks)} chunks...")
        
        # Create embeddings for all chunks at once (more efficient)
        embeddings = self.embedding_model.encode(all_chunks, show_progress_bar=True)
        
        # Convert embeddings to list format for ChromaDB
        embeddings_list = embeddings.tolist()
        
        print("Storing in vector database...")
        
        # Add to ChromaDB collection
        self.collection.add(
            embeddings=embeddings_list,
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )
        
        # Get collection info
        collection_count = self.collection.count()
        
        print(f"Successfully added {len(all_chunks)} chunks to vector database")
        print(f"Total documents in collection: {collection_count}")
        print("Documents added to vector database")

    def search(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Search for similar documents in the vector database.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            Dictionary containing search results with keys: 'documents', 'metadatas', 'distances', 'ids'
        """
        if not query or not query.strip():
            print("Empty query provided")
            return {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "ids": [],
            }
        
        # Check if collection has any data
        collection_count = self.collection.count()
        if collection_count == 0:
            print("No documents in the collection to search")
            return {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "ids": [],
            }
        
        try:
            print(f"Searching for: '{query}' (returning top {n_results} results)")
            
            # Create embedding for the query
            query_embedding = self.embedding_model.encode([query])
            
            # Convert to list format for ChromaDB
            query_embedding_list = query_embedding.tolist()
            
            # Ensure n_results doesn't exceed available documents
            actual_n_results = min(n_results, collection_count)
            
            # Search in ChromaDB collection
            results = self.collection.query(
                query_embeddings=query_embedding_list,
                n_results=actual_n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            # ChromaDB returns lists of lists, so we need to flatten them
            # Since we're querying with a single query, we take the first (and only) result set
            search_results = {
                "documents": results['documents'][0] if results['documents'] else [],
                "metadatas": results['metadatas'][0] if results['metadatas'] else [],
                "distances": results['distances'][0] if results['distances'] else [],
                "ids": results['ids'][0] if results['ids'] else [],
            }
            
            print(f"Found {len(search_results['documents'])} relevant chunks")
            
            # Print results summary for debugging
            for i, (doc, distance, metadata) in enumerate(zip(
                search_results['documents'][:3],  # Show first 3 results
                search_results['distances'][:3],
                search_results['metadatas'][:3]
            )):
                print(f"  Result {i+1}: {metadata.get('document_name', 'Unknown')} "
                      f"(distance: {distance:.3f}) - {doc[:100]}...")
            
            return search_results
            
        except Exception as e:
            print(f"Error during search: {e}")
            return {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "ids": [],
            }
