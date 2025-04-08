import os
import argparse
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def setup_environment():
    """Set up the environment for the GPRMax RAGBot."""
    # Create necessary directories
    directories = [
        "data",
        "docs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    # Check for .env file
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            logger.info("Creating .env file from .env.example")
            with open(".env.example", "r") as example_file:
                example_content = example_file.read()
            
            with open(".env", "w") as env_file:
                env_file.write(example_content)
            
            logger.info("Created .env file. Please update it with your API keys.")
        else:
            logger.warning(".env.example file not found. Please create a .env file manually.")
    else:
        logger.info(".env file already exists.")
    
    logger.info("Environment setup complete.")

def check_openai_key():
    """Check if the OpenAI API key is set."""
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key or openai_key == "your_openai_api_key_here":
        logger.warning("OpenAI API key not set. Please update the .env file with your API key.")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Set up the GPRMax RAGBot environment")
    parser.add_argument(
        "--check-only", 
        action="store_true", 
        help="Only check the environment without making changes"
    )
    
    args = parser.parse_args()
    
    if args.check_only:
        # Just check if OpenAI key is set
        if check_openai_key():
            logger.info("Environment check passed.")
        else:
            logger.warning("Environment check failed.")
    else:
        # Set up the environment
        setup_environment()
        check_openai_key()

if __name__ == "__main__":
    main()
