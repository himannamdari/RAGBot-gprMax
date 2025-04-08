import os
import streamlit as st
from dotenv import load_dotenv
from rag_engine import GPRMaxRAGEngine

# Load environment variables
load_dotenv()

# Initialize the RAG engine
@st.cache_resource
def initialize_rag_engine():
    return GPRMaxRAGEngine()

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

# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your GPRMax assistant. How can I help you with your Ground Penetrating Radar simulations today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize RAG engine
rag_engine = initialize_rag_engine()

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
