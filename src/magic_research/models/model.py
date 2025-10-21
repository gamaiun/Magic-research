import os
from typing import List
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from ..data import VectorDB, load_pdf_documents
except ImportError:
    # Fallback for direct execution or when importing from project root
    import sys
    import os
    
    # Add the magic_research directory to sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    magic_research_dir = os.path.dirname(current_dir)  # Go up from models/
    sys.path.insert(0, magic_research_dir)
    
    from data import VectorDB, load_pdf_documents

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
# Load environment variables
load_dotenv()


def load_documents() -> List[str]:
    """
    Load PDF documents using the data processing modules.

    Returns:
        List of formatted document strings
    """
    # Use the new data processing module
    return load_pdf_documents()


class RAGAssistant:
    """
    A simple RAG-based AI assistant using ChromaDB and multiple LLM providers.
    Supports OpenAI, Groq, and Google Gemini APIs.
    """

    def __init__(self):
        """Initialize the RAG assistant."""
        # Initialize LLM - check for available API keys in order of preference
        self.llm = self._initialize_llm()
        if not self.llm:
            raise ValueError(
                "No valid API key found. Please set one of: "
                "OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY in your .env file"
            )

        # Initialize vector database
        self.vector_db = VectorDB()

        # Create RAG prompt template
        template = """You are a helpful AI assistant specializing in academic research and publications.

Your task is to answer questions based ONLY on the provided publication content below. 

IMPORTANT GUIDELINES:
- Base your answers exclusively on the information provided in the publication content
- If the information is not available in the provided content, clearly state that you cannot answer based on the available material
- Provide specific references or quotes when possible
- Be accurate and scholarly in your responses
- If multiple perspectives are presented in the content, acknowledge them

PUBLICATION CONTENT:
{context}

QUESTION: {question}

ANSWER:"""
        
        self.prompt_template = ChatPromptTemplate.from_template(template)

        # Create the chain
        self.chain = self.prompt_template | self.llm | StrOutputParser()

        print("RAG Assistant initialized successfully")

    def _initialize_llm(self):
        """
        Initialize the LLM by checking for available API keys.
        Tries OpenAI, Groq, and Google Gemini in that order.
        """
        # Check for OpenAI API key
        if os.getenv("OPENAI_API_KEY"):
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            print(f"Using OpenAI model: {model_name}")
            return ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"), model=model_name, temperature=0.0
            )

        elif os.getenv("GROQ_API_KEY"):
            model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
            print(f"Using Groq model: {model_name}")
            return ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"), model=model_name, temperature=0.0
            )

        elif os.getenv("GOOGLE_API_KEY"):
            model_name = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
            print(f"Using Google Gemini model: {model_name}")
            return ChatGoogleGenerativeAI(
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                model=model_name,
                temperature=0.0,
            )

        else:
            raise ValueError(
                "No valid API key found. Please set one of: OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY in your .env file"
            )

    def add_documents(self, documents: List) -> None:
        """
        Add documents to the knowledge base.

        Args:
            documents: List of documents
        """
        self.vector_db.add_documents(documents)
    
    def get_document_count(self) -> int:
        """
        Get the number of documents currently in the vector database.
        
        Returns:
            Number of document chunks in the database
        """
        return self.vector_db.collection.count()
    
    def clear_documents(self) -> None:
        """
        Clear all documents from the vector database.
        Useful for starting fresh or updating the knowledge base.
        """
        # Delete the collection and recreate it
        self.vector_db.client.delete_collection(name=self.vector_db.collection_name)
        self.vector_db.collection = self.vector_db.client.get_or_create_collection(
            name=self.vector_db.collection_name,
            metadata={"description": "RAG document collection"},
        )
        print("✅ Vector database cleared successfully")

    def invoke(self, input: str, n_results: int = 3) -> str:
        """
        Query the RAG assistant.

        Args:
            input: User's input
            n_results: Number of relevant chunks to retrieve

        Returns:
            String containing the LLM's answer based on retrieved context
        """
        if not input or not input.strip():
            return "Please provide a valid question."
        
        try:
            print(f"Processing query: '{input}'")
            
            # Step 1: Search for relevant context chunks
            search_results = self.vector_db.search(input, n_results=n_results)
            
            if not search_results['documents']:
                return "I couldn't find any relevant information in the knowledge base to answer your question."
            
            # Step 2: Combine retrieved chunks into context string
            context_chunks = []
            print(f"\nRetrieved {len(search_results['documents'])} relevant chunks:")
            
            for i, (doc, metadata, distance) in enumerate(zip(
                search_results['documents'],
                search_results['metadatas'], 
                search_results['distances']
            )):
                # Add chunk with source information
                source_info = f"[Source: {metadata.get('document_name', 'Unknown document')}, Chunk {metadata.get('chunk_index', 'N/A')}]"
                context_chunk = f"{source_info}\n{doc}\n"
                context_chunks.append(context_chunk)
                
                print(f"  {i+1}. From {metadata.get('document_name', 'Unknown')} (distance: {distance:.3f})")
            
            # Combine all context chunks
            context = "\n---\n".join(context_chunks)
            
            # Step 3: Generate response using the LLM chain
            print("\nGenerating response...")
            llm_answer = self.chain.invoke({
                "context": context,
                "question": input
            })
            
            return llm_answer
            
        except Exception as e:
            print(f"Error during query processing: {e}")
            return f"I encountered an error while processing your question: {str(e)}"


def main():
    """Main function to demonstrate the RAG assistant."""
    try:
        # Initialize the RAG assistant
        print("Initializing RAG Assistant...")
        assistant = RAGAssistant()

        # Check if documents are already in the database
        current_count = assistant.vector_db.collection.count()
        print(f"Current documents in vector database: {current_count}")
        
        if current_count == 0:
            # Load and add documents only if database is empty
            print("\nDatabase is empty. Loading documents...")
            sample_docs = load_documents()
            print(f"Loaded {len(sample_docs)} sample documents")
            assistant.add_documents(sample_docs)
        else:
            print("Documents already exist in database. Skipping document loading.")
            print("✅ Ready to answer questions!")

        done = False

        while not done:
            question = input("Enter a question or 'quit' to exit: ")
            if question.lower() == "quit":
                done = True
            else:
                result = assistant.invoke(question)
                print(f"\nAnswer: {result}\n")

    except Exception as e:
        print(f"Error running RAG assistant: {e}")
        print("Make sure you have set up your .env file with at least one API key:")
        print("- OPENAI_API_KEY (OpenAI GPT models)")
        print("- GROQ_API_KEY (Groq Llama models)")
        print("- GOOGLE_API_KEY (Google Gemini models)")


if __name__ == "__main__":
    main()
