import pypdf
import logging
import os

logger = logging.getLogger(__name__)

def extract_text_from_pdfs(source_dir_or_file):
    """
    Extracts text from a single PDF file or a directory of PDFs.
    
    Args:
        source_dir_or_file (str): Path to a directory or a single PDF file.
        
    Returns:
        dict: A dictionary where key is filename and value is extracted text.
    """
    extracted_data = {}
    
    # helper to process one file
    def process_file(file_path):
        try:
            logger.info(f"Extracting text from: {file_path}")
            text = ""
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}")
            return None

    if os.path.isfile(source_dir_or_file):
        filename = os.path.basename(source_dir_or_file)
        text = process_file(source_dir_or_file)
        if text:
            extracted_data[filename] = text
            
    elif os.path.isdir(source_dir_or_file):
        for root, dirs, files in os.walk(source_dir_or_file):
            for file in files:
                if file.lower().endswith(".pdf"):
                    full_path = os.path.join(root, file)
                    text = process_file(full_path)
                    if text:
                        extracted_data[file] = text

    return extracted_data
