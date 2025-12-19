import os
import sys
import argparse

# Add the project root to the python path to allow imports if running from subdirs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import GROQ_API_KEY
from ingestion.excel_processor import load_training_plan
from ingestion.web_content import fetch_saica_framework
from ingestion.context_loader import load_all_context
from analysis.mapper import map_activity_to_competency
from reporting.generator import create_report
from utils.logger import setup_logger

logger = setup_logger()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "Documents for training")
EXCEL_PATH = os.path.join(DOCS_DIR, "Training plan", "Training-plan-template.xlsx")

SAICA_URLS = [
    "https://www.saica.org.za/initiatives/competency-framework",
    "https://www.saica.org.za/resources/training-offices"
]

def main():
    parser = argparse.ArgumentParser(description="SAICA Competency Mapping Agent")
    parser.add_argument("--input", type=str, help="Trainee activity description", default=None)
    args = parser.parse_args()

    logger.info("Starting SAICA_Scribe (Competency Mapping Agent)...")

    # 1. Ingestion: Training Plan (Excel)
    logger.info(f"Ingesting Training Plan from: {EXCEL_PATH}")
    if os.path.exists(EXCEL_PATH):
        training_plan = load_training_plan(EXCEL_PATH)
        logger.info(f"Loaded {len(training_plan)} items from Training Plan.")
    else:
        logger.error(f"Training Plan file not found at {EXCEL_PATH}")
        training_plan = []

    # 2. Ingestion: SAICA Website Content
    logger.info("Ingesting SAICA Framework content from web...")
    web_content = fetch_saica_framework(SAICA_URLS)
    
    # 3. Ingestion: Enhanced Context (Guidelines/Examples)
    logger.info("Ingesting Guidelines and Context documents...")
    additional_context = load_all_context(DOCS_DIR)

    # 4. Input: Trainee Activity
    if args.input:
        trainee_input = args.input
    else:
        print("\n" + "="*50)
        trainee_input = input("Please describe the activity you performed: ")
        print("="*50 + "\n")
    
    if not trainee_input.strip():
        logger.warning("No input provided. Exiting.")
        return

    logger.info(f"Processing trainee input: '{trainee_input}'")

    # 5. Analysis: Mapping
    framework_data = {
        "training_plan": training_plan,
        "web_content": web_content,
        "additional_context": additional_context
    }
    
    logger.info("Mapping activity to competencies...")
    mapping_result = map_activity_to_competency(trainee_input, framework_data)

    # 6. Reporting
    logger.info("Generating report...")
    report_path = create_report(mapping_result)
    logger.info(f"Report created at: {report_path}")
    print(f"\n✅ Report generated successfully: {report_path}\n")

    logger.info("Done.")

if __name__ == "__main__":
    main()
