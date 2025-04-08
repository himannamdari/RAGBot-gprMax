import os
import streamlit as st
from dotenv import load_dotenv
import logging
import subprocess
import time
from rag_engine import GPRMaxRAGEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set OpenAI API key via Streamlit
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# Function to check if PDF is available and run ingestion if needed
def check_and_prepare_data():
    # Check for the vector database
    if not os.path.exists("data/vector_db"):
        st.warning("Vector database not found. The system needs to process the gprMax documentation first.")
        
        # Check if PDF exists
        pdf_path = "docs/docs-gprmax-com-en-latest.pdf"
        pdf_exists = os.path.exists(pdf_path)
        
        if not pdf_exists:
            st.error(f"gprMax documentation PDF not found at {pdf_path}. Please upload it below:")
            uploaded_file = st.file_uploader("Upload gprMax Documentation PDF", type="pdf")
            
            if uploaded_file is not None:
                # Create docs directory if it doesn't exist
                os.makedirs("docs", exist_ok=True)
                
                # Save the uploaded file
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File saved to {pdf_path}")
                pdf_exists = True
            else:
                return False
        
        # Run ingestion if PDF exists
        if pdf_exists:
            with st.spinner("Processing documentation... This may take a few minutes..."):
                try:
                    # Import and run the ingest module
                    from ingest import process_documents, create_vector_store
                    
                    # Process documents
                    document_chunks = process_documents(pdf_path)
                    
                    # Create vector store
                    create_vector_store(document_chunks)
                    
                    st.success("Documentation processed successfully!")
                    return True
                except Exception as e:
                    st.error(f"Error processing documentation: {str(e)}")
                    logger.error(f"Error processing documentation: {str(e)}")
                    return False
        return False
    return True

# Initialize the RAG engine
@st.cache_resource
def initialize_rag_engine():
    # Check if vector store exists
    if os.path.exists("data/vector_db"):
        return GPRMaxRAGEngine()
    return None

# Page configuration
st.set_page_config(
    page_title="GPRMax RAGBot",
    page_icon="📡",
    layout="wide"
)

# Main title
st.title("📡 GPRMax RAGBot")
st.markdown("### Your AI assistant for GPR simulations")

# Sidebar with information
with st.sidebar:
    st.title("About")
    st.info(
        """
        This AI assistant is trained on the gprMax documentation to help you:
        - Learn about gprMax features
        - Get guidance on model setup
        - Troubleshoot common issues
        - Understand GPR simulation concepts
        
        [gprMax Official Website](https://www.gprmax.com/)
        """
    )
    
    st.markdown("### Examples")
    example_questions = [
        "How do I install gprMax?",
        "What are the essential commands for input files?",
        "How do I model a heterogeneous soil?",
        "Explain the PML absorbing boundary conditions",
        "How can I visualize my results?",
    ]
    
    for q in example_questions:
        if st.button(q):
            st.session_state["user_input"] = q
            st.experimental_rerun()

# Check if data is prepared
data_ready = check_and_prepare_data()

if not data_ready:
    st.warning("Please upload the gprMax documentation to proceed.")
else:
    # Initialize RAG engine
    rag_engine = initialize_rag_engine()
    
    if rag_engine is None:
        st.error("Failed to initialize RAG engine. Please check the logs for details.")
    else:
        # Initialize chat history if not already present
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your GPRMax assistant. How can I help you with your Ground Penetrating Radar simulations today?"}
            ]

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        if "user_input" in st.session_state:
            user_input = st.session_state.user_input
            del st.session_state.user_input
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Generate response using RAG engine
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response_container = st.empty()
                    response, sources = rag_engine.generate_response(user_input)
                    response_container.markdown(response)
                    
                    # If there are sources, display them
                    if sources:
                        st.markdown("#### Sources")
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"{i}. {source}")
            
            # Add assistant response to chat history
            full_response = response
            if sources:
                full_response += "\n\n**Sources:**\n" + "\n".join([f"{i}. {source}" for i, source in enumerate(sources, 1)])
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Input box for new questions
        user_input = st.chat_input("Ask me about gprMax...")
        if user_input:
            st.session_state.user_input = user_input
            st.experimental_rerun()
