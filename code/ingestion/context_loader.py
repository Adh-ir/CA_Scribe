import os
import logging
from ingestion.pdf_processor import extract_text_from_pdfs
try:
    from docx import Document
except ImportError:
    Document = None

logger = logging.getLogger(__name__)

# Define the specific subdirectories provided by user
CONTEXT_DIRS = [
    "Review of compentencies",
    "How to write out compentencies",
    "Mapping",
    "prompt"  # <--- CRITICAL: Added prompt directory
]

def extract_text_from_docx(directory):
    """
    Extracts text from all .docx files in the given directory.
    """
    texts = {}
    if not os.path.exists(directory):
        return texts

    if Document is None:
        logger.warning("python-docx not installed. Skipping .docx files.")
        return texts

    for filename in os.listdir(directory):
        if filename.lower().endswith('.docx') and not filename.startswith('~$'):
            file_path = os.path.join(directory, filename)
            try:
                doc = Document(file_path)
                full_text = []
                for para in doc.paragraphs:
                    full_text.append(para.text)
                texts[filename] = "\n".join(full_text)
                logger.info(f"Extracted {len(texts[filename])} chars from {filename}")
            except Exception as e:
                logger.error(f"Failed to read docx {filename}: {e}")
    return texts

def load_all_context(base_dir):
    """
    Loads text content from the simplified 'Documents for training' folder structure.
    Specifically looks into the defined CONTEXT_DIRS.
    
    Args:
        base_dir (str): The root path to 'Documents for training'.
        
    Returns:
        dict: A dictionary structured by 'category' (folder name) -> 'files' (dict of texts).
    """
    context_data = {}

    for subdir in CONTEXT_DIRS:
        full_path = os.path.join(base_dir, subdir)
        if not os.path.exists(full_path):
            logger.warning(f"Context directory not found: {full_path}")
            continue
            
        logger.info(f"Loading context from: {subdir}")
        
        # 1. Load PDFs
        subdir_texts = extract_text_from_pdfs(full_path)
        
        # 2. Load Docx
        docx_texts = extract_text_from_docx(full_path)
        subdir_texts.update(docx_texts)
        
        if subdir_texts:
            context_data[subdir] = subdir_texts
            
    return context_data
