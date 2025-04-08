import os
import json
import logging
from typing import List, Dict, Any
import argparse
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def process_documents(docs_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Any]:
    """
    Process documents (PDF and text files) from a directory.
    
    Args:
        docs_dir: Directory containing the documents
        chunk_size: Size of text chunks for splitting
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document chunks
    """
    logger.info(f"Processing documents from {docs_dir}")
    
    # Load documents
    documents = []
    
    # Check if docs_dir is a file or directory
    if os.path.isfile(docs_dir):
        if docs_dir.endswith('.pdf'):
            logger.info(f"Loading PDF file: {docs_dir}")
            loader = PyPDFLoader(docs_dir)
            documents.extend(loader.load())
        elif docs_dir.endswith('.txt'):
            logger.info(f"Loading text file: {docs_dir}")
            loader = TextLoader(docs_dir)
            documents.extend(loader.load())
    else:
        # Load PDFs
        pdf_loader = DirectoryLoader(docs_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
        documents.extend(pdf_loader.load())
        
        # Load text files
        txt_loader = DirectoryLoader(docs_dir, glob="**/*.txt", loader_cls=TextLoader)
        documents.extend(txt_loader.load())
    
    logger.info(f"Loaded {len(documents)} documents")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    document_chunks = text_splitter.split_documents(documents)
    logger.info(f"Created {len(document_chunks)} document chunks")
    
    return document_chunks

def create_vector_store(document_chunks: List[Any], vector_db_path: str = "data/vector_db") -> None:
    """
    Create and save a vector store from document chunks.
    
    Args:
        document_chunks: List of document chunks
        vector_db_path: Path to save the vector database
    """
    logger.info("Creating vector store")
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create vector store
    vector_store = FAISS.from_documents(document_chunks, embeddings)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(vector_db_path), exist_ok=True)
    
    # Save vector store
    vector_store.save_local(vector_db_path)
    logger.info(f"Vector store saved to {vector_db_path}")

def main():
    parser = argparse.ArgumentParser(description="Ingest documents for GPRMax RAGBot")
    parser.add_argument(
        "--docs-dir", 
        type=str, 
        default="docs", 
        help="Directory containing the documents to process"
    )
    parser.add_argument(
        "--vector-db-path", 
        type=str, 
        default="data/vector_db", 
        help="Path to save the vector database"
    )
    parser.add_argument(
        "--chunk-size", 
        type=int, 
        default=1000, 
        help="Size of text chunks for splitting"
    )
    parser.add_argument(
        "--chunk-overlap", 
        type=int, 
        default=200, 
        help="Overlap between chunks"
    )
    
    args = parser.parse_args()
    
    # Process documents
    document_chunks = process_documents(
        args.docs_dir, 
        chunk_size=args.chunk_size, 
        chunk_overlap=args.chunk_overlap
    )
    
    # Create vector store
    create_vector_store(document_chunks, args.vector_db_path)
    
    logger.info("Document ingestion complete")

if __name__ == "__main__":
    main()
