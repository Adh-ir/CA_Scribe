import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.excel_processor import load_training_plan

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "Documents for training", "Training plan", "Training-plan-template.xlsx")

def list_all_competencies():
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: File not found at {EXCEL_PATH}")
        return

    print("Loading Training Plan...")
    plan = load_training_plan(EXCEL_PATH)
    
    print(f"\nFound {len(plan)} total rows to check.\n")
    if len(plan) > 1:
        print("Second item sample (Row 1):", plan[1])
    
    print(f"{'INDEX':<6} | {'LEVEL':<6} | {'AREA':<20} | {'COMPETENCY'}")
    print("-" * 120)

    count = 0
    for idx, item in enumerate(plan):
        level = item.get("SAICA required level")
        if level == 0 or level == "0":
            continue
            
        # Based on inspection:
        # Unnamed: 6 -> Description of the task
        # Unnamed: 4 -> Category Name (e.g. Personal Ethics)
        # Unnamed: 2 -> Higher Level Group (e.g. Ethics)
        
        description = str(item.get('Unnamed: 6', ''))
        category = str(item.get('Unnamed: 4', ''))
        
        # Clean naming
        if category == 'nan': category = ""
        if description == 'nan': description = ""
        
        # Truncate for display
        print(f"{idx:<6} | {str(level):<6} | {category[:25]:<25} | {description}")
        count += 1
        
    print("-" * 80)
    print(f"\nTotal Active Competencies (Level > 0): {count}")

if __name__ == "__main__":
    list_all_competencies()
