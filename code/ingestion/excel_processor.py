import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_training_plan(file_path):
    """
    Reads the 'ELP' tab from the Training Plan Excel file.
    
    Args:
        file_path (str): Absolute path to the .xlsx file.
        
    Returns:
        list: A list of dictionaries representing the competencies/tasks.
    """
    try:
        logger.info(f"Loading training plan from: {file_path}")
        # Read the "ELP" sheet
        # Note: We need to verify if the sheet name is exactly "ELP" or has spaces.
        df = pd.read_excel(file_path, sheet_name="ELP")
        
        # Convert to records to essentially get a list of rows
        records = df.to_dict(orient='records')
        logger.info(f"Successfully loaded {len(records)} records from ELP tab.")
        return records

    except Exception as e:
        logger.error(f"Failed to load training plan: {e}")
        return []
