# GPRMax RAGBot

A Retrieval-Augmented Generation (RAG) chatbot to help researchers use gprMax effectively.

## Overview

The GPRMax RAGBot is designed to assist researchers in using gprMax, a Ground Penetrating Radar (GPR) simulation software. It uses Retrieval-Augmented Generation (RAG) to provide accurate information by combining the power of Large Language Models (LLMs) with the specific knowledge contained in the gprMax documentation.

## Features

- **Contextual Understanding**: Understands and responds to queries about gprMax with context from the official documentation
- **Interactive Interface**: Provides an intuitive Streamlit web interface for easy interaction
- **Citation Support**: Includes references to the relevant documentation sections
- **Real-time Assistance**: Offers immediate help for common issues and questions

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/gprmax-ragbot.git
cd gprmax-ragbot
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root directory
   - Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Ask questions about gprMax, its features, or how to use it for specific GPR simulations

## Project Structure

- `app.py`: Main Streamlit application
- `ingest.py`: Scripts for data ingestion and processing
- `rag_engine.py`: Core RAG implementation
- `utils.py`: Utility functions
- `data/`: Directory containing processed document chunks
- `docs/`: Original gprMax documentation

## Dependencies

- Python 3.8+
- Streamlit
- LangChain
- OpenAI API
- FAISS vector store
- dotenv

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- gprMax documentation and team: [gprMax.com](https://www.gprmax.com/)
- Built with [Streamlit](https://streamlit.io/) and [LangChain](https://langchain.com/)
