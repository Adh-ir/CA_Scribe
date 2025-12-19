import os

# Configuration Settings

# SAICA_Scribe Configuration

import os
from dotenv import load_dotenv, set_key

# Load environment variables from .env file
load_dotenv()

# AI Configuration
# NOTE: Keys are managed via the Web UI (Setup Wizard).
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Defaults
GEMINI_MODEL = "gemini-flash-latest"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini") # Options: "gemini", "groq"

def save_keys(google_key=None, groq_key=None, provider=None):
    """
    Saves API keys to the local .env file.
    """
    env_file = ".env"
    if not os.path.exists(env_file):
        open(env_file, 'w').close()
    
    # Load existing to not overwrite other things if they existed
    load_dotenv(env_file)

    if google_key and google_key.strip():
        set_key(env_file, "GOOGLE_API_KEY", google_key.strip())
        os.environ["GOOGLE_API_KEY"] = google_key.strip()
        
    if groq_key and groq_key.strip():
        set_key(env_file, "GROQ_API_KEY", groq_key.strip())
        os.environ["GROQ_API_KEY"] = groq_key.strip()
        
    if provider:
        set_key(env_file, "LLM_PROVIDER", provider)
        os.environ["LLM_PROVIDER"] = provider

# Paths
DATA_DIR = "data"
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
OUTPUT_DIR = "output"
