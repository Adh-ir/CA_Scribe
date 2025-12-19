import logging
import sys
import os

# Setup logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Add code dir to path
sys.path.append(os.path.join(os.getcwd(), 'code'))

from ingestion.excel_processor import load_training_plan

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "code", "Documents for training", "Training plan", "Training-plan-template.xlsx")

print(f"Testing loader with path: {EXCEL_PATH}")

try:
    records = load_training_plan(EXCEL_PATH)
    print(f"\nResult: Loaded {len(records)} records.")
    if records:
        print("Sample:", records[0])
except Exception as e:
    print(f"\nCRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
