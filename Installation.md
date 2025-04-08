# Installation Guide

This guide will walk you through the process of setting up the GPRMax RAGBot on your system.

## Prerequisites

Before getting started, make sure you have the following:

- Python 3.8 or higher
- pip (Python package installer)
- An OpenAI API key

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/gprmax-ragbot.git
cd gprmax-ragbot
```

## Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment is recommended to avoid conflicts with other Python packages:

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your favorite text editor and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Step 5: Prepare the Documentation

1. Place the gprMax documentation PDF in the `docs` directory:
```bash
mkdir -p docs
# Copy the gprMax documentation PDF to the docs directory
cp path/to/docs-gprmax-com-en-latest.pdf docs/
```

## Step 6: Process the Documentation

Run the data ingestion script to process the documentation and create the vector database:

```bash
python ingest.py --docs-dir docs/docs-gprmax-com-en-latest.pdf
```

This step may take a few minutes depending on the size of the documentation.

## Step 7: Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application should now be accessible in your web browser at http://localhost:8501.

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError" when running the application**:
   - Make sure you've installed all dependencies with `pip install -r requirements.txt`
   - Ensure your virtual environment is activated

2. **"Error loading vector database"**:
   - Ensure you've run the ingestion script before starting the application
   - Check if the `data/vector_db` directory exists and contains files

3. **"API key not configured" error**:
   - Make sure you've set up your `.env` file with a valid OpenAI API key
   - Check that the `.env` file is in the root directory of the project

4. **"Out of memory" error during ingestion**:
   - Try reducing the chunk size in the ingestion script with `--chunk-size 500`

For additional help, please open an issue on the GitHub repository.
