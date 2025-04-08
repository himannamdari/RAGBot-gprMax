import os
import json
from typing import List, Tuple, Dict, Any
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


os.environ["OPENAI_API_KEY"] = "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" 




class GPRMaxRAGEngine:
    """Engine handling retrieval-augmented generation for gprMax queries."""
    
    def __init__(self, vector_db_path: str = "data/vector_db", 
                 model_name: str = "gpt-4", temperature: float = 0.0):
        """
        Initialize the RAG engine.
        
        Args:
            vector_db_path: Path to the vector database
            model_name: OpenAI model to use
            temperature: Model temperature (0.0 for more deterministic outputs)
        """
        self.embeddings = OpenAIEmbeddings()
        
        # Load vector store if it exists
        if os.path.exists(vector_db_path):
            self.vector_store = FAISS.load_local(vector_db_path, self.embeddings)
        else:
            raise FileNotFoundError(f"Vector database not found at {vector_db_path}. Run ingest.py first.")
        
        # Initialize retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        
        # Create the QA prompt
        self.qa_prompt = PromptTemplate(
            template="""You are an expert assistant for gprMax, a Ground Penetrating Radar (GPR) simulation software. 
            Your task is to answer the user's question based on the provided context from the gprMax documentation.
            
            If the answer is not in the context, politely state that you don't have information about that specific topic 
            and suggest they check the official gprMax documentation or website.
            
            When providing code examples or explaining commands, format code blocks properly with appropriate markdown.
            Be precise in your explanations and make sure to organize your response in a clear and structured manner.
            
            Context:
            {context}
            
            Question:
            {question}
            
            Answer:""",
            input_variables=["context", "question"]
        )
        
        # Create the QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.qa_prompt}
        )
    
    def generate_response(self, query: str) -> Tuple[str, List[str]]:
        """
        Generate a response for the query using the RAG system.
        
        Args:
            query: User's question about gprMax
            
        Returns:
            Tuple containing the response text and a list of sources
        """
        # Run the query through the QA chain
        result = self.qa_chain({"query": query})
        
        # Extract the answer
        answer = result.get("result", "I couldn't generate a response. Please try rephrasing your question.")
        
        # Extract and format sources
        source_documents = result.get("source_documents", [])
        sources = []
        
        for doc in source_documents:
            # Extract metadata
            metadata = doc.metadata
            section = metadata.get("section", "Unknown section")
            page = metadata.get("page", "Unknown page")
            
            # Format source information
            source_info = f"Section: {section}, Page: {page}"
            if source_info not in sources:
                sources.append(source_info)
        
        return answer, sources
