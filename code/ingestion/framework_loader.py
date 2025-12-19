import os
import logging
from ingestion.excel_processor import load_training_plan
from ingestion.web_content import fetch_saica_framework
from ingestion.context_loader import load_all_context

logger = logging.getLogger(__name__)

# Paths - Relative to Project Root (assuming run from root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "Documents for training")
EXCEL_PATH = os.path.join(DOCS_DIR, "Training plan", "Training-plan-template.xlsx")

SAICA_URLS = [
    "https://www.saica.org.za/initiatives/competency-framework",
    "https://www.saica.org.za/resources/training-offices"
]

def load_saica_framework():
    """
    Loads all SAICA framework data (Training Plan, Web Content, Context).
    Returns a dictionary suitable for the mapper.
    """
    logger.info("Loading SAICA Framework Data...")
    
    # 1. Training Plan
    if os.path.exists(EXCEL_PATH):
        training_plan = load_training_plan(EXCEL_PATH)
        logger.info(f"Loaded {len(training_plan)} items from Training Plan.")
    else:
        logger.error(f"Training Plan file not found at {EXCEL_PATH}")
        training_plan = []
        
    # 2. Web Content
    web_content = fetch_saica_framework(SAICA_URLS)
    
    # 3. Enhanced Context
    additional_context = load_all_context(DOCS_DIR)
    
    return {
        "training_plan": training_plan,
        "web_content": web_content,
        "additional_context": additional_context
    }
