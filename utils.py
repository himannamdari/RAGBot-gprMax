import os
import logging
from typing import Dict, List, Any, Optional
import json
import tiktoken

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Count the number of tokens in a text string.
    
    Args:
        text: Text to count tokens for
        model: Model name to use for tokenization
        
    Returns:
        Number of tokens
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def extract_metadata_from_page(page_content: str, page_num: int) -> Dict[str, Any]:
    """
    Extract metadata from page content.
    
    Args:
        page_content: Content of the page
        page_num: Page number
        
    Returns:
        Dictionary containing metadata
    """
    # Initialize metadata
    metadata = {
        "page": page_num,
        "section": "Unknown"
    }
    
    # Try to extract section from heading
    lines = page_content.strip().split('\n')
    if lines:
        # Look for section titles (headings)
        for line in lines[:5]:  # Check first few lines
            line = line.strip()
            if line and (line.isupper() or line.startswith('#') or line.endswith(':')):
                metadata["section"] = line.replace('#', '').strip()
                break
    
    return metadata

def save_json(data: Any, file_path: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save the file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save data
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Data saved to {file_path}")

def load_json(file_path: str) -> Optional[Any]:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Loaded data or None if file doesn't exist
    """
    if not os.path.exists(file_path):
        logger.warning(f"File {file_path} does not exist")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.info(f"Data loaded from {file_path}")
    return data

def format_source_reference(doc: Any) -> str:
    """
    Format a source reference from a document.
    
    Args:
        doc: Document to format
        
    Returns:
        Formatted source reference
    """
    metadata = doc.metadata
    section = metadata.get("section", "Unknown section")
    page = metadata.get("page", "Unknown page")
    
    return f"Section: {section} (Page {page})"
