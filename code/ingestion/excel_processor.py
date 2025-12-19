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
        
        # Clean and Map
        clean_records = []
        for _, row in df.iterrows():
            # Skip if critical fields are empty
            if pd.isna(row.get('Competency')) and pd.isna(row.get('Learning outcome')):
                continue
                
            # Construct standard keys
            # Code: Combine ID/Competency with Outcome (e.g. "1.1 (a)")
            comp_id = str(row.get('Id') or row.get('Competency') or '').replace('.0', '').strip()
            outcome = str(row.get('Learning outcome') or '').strip()
            
            code = f"{comp_id}{outcome}"
            
            # Clean Name
            # Try Unnamed: 4 (Specific) -> Unnamed: 2 (Group) -> Code itself
            raw_name_4 = row.get('Unnamed: 4')
            raw_name_2 = row.get('Unnamed: 2')
            
            def clean_str(val):
                if pd.isna(val): return ""
                s = str(val).strip()
                if s.lower() == 'nan': return ""
                return s

            name = clean_str(raw_name_4)
            if not name:
                name = clean_str(raw_name_2)
            if not name:
                name = f"Competency {code}" # Last resort fallback vs "Unknown"

            desc = clean_str(row.get('Unnamed: 6'))
            
            clean_records.append({
                "competency_code": code,
                "competency_name": name,
                "behavioral_indicators": desc,
                "original_row": row.to_dict() # debug/fallback
            })
            
        logger.info(f"Successfully loaded {len(clean_records)} clean records from ELP tab.")
        return clean_records

    except Exception as e:
        logger.error(f"Failed to load training plan: {e}")
        return []
