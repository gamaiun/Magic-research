#!/usr/bin/env python3
"""
Script to reload PDF documents into the vector database.
This will clear any existing data and reload from PDFs in the data/ directory.
"""

import os
import sys

# Add src to Python path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from magic_research.models.model import load_documents
from magic_research.data import VectorDB

def main():
    """Force reload all PDF documents."""
    print("🔄 Reloading PDF documents into vector database...")
    
    try:
        # Initialize vector database
        print("Initializing vector database...")
        vector_db = VectorDB()
        
        # Clear existing collection
        collection_count = vector_db.collection.count()
        if collection_count > 0:
            print(f"Found {collection_count} existing documents. Clearing database...")
            # Delete the collection and recreate it
            vector_db.client.delete_collection(vector_db.collection_name)
            vector_db.collection = vector_db.client.get_or_create_collection(
                name=vector_db.collection_name,
                metadata={"description": "RAG document collection"},
            )
            print("✅ Database cleared")
        
        # Load documents from PDFs
        print("Loading PDF documents...")
        documents = load_documents()
        
        if not documents:
            print("❌ No documents loaded! Check that PDF files exist in data/ directory")
            return
            
        print(f"Loaded {len(documents)} documents")
        
        # Add documents to vector database
        print("Adding documents to vector database...")
        vector_db.add_documents(documents)
        
        # Verify the results
        final_count = vector_db.collection.count()
        print(f"✅ Successfully loaded {final_count} document chunks into vector database")
        
        # Test search
        print("\n🔍 Testing search functionality...")
        test_results = vector_db.search("Abraham of Worms", n_results=3)
        
        if test_results['documents']:
            print(f"Found {len(test_results['documents'])} results for 'Abraham of Worms':")
            for i, (doc, metadata) in enumerate(zip(test_results['documents'][:2], test_results['metadatas'][:2])):
                doc_name = metadata.get('document_name', 'Unknown')
                print(f"  {i+1}. From {doc_name}: {doc[:100]}...")
        else:
            print("❌ No results found for test search")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    print("\n🎉 PDF reload complete!")
    return 0

if __name__ == "__main__":
    exit(main())