"""
=========================================
Customer Churn Prediction Configuration
=========================================
"""

from pathlib import Path

# ==========================
# Project Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA_PATH = DATA_DIR / "raw" / "Customer_Churn.csv"

PROCESSED_DATA_PATH = DATA_DIR / "processed" / "customer_churn_clean.csv"

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "churn_model.pkl"

OUTPUT_DIR = BASE_DIR / "outputs"

GRAPH_DIR = OUTPUT_DIR / "graphs"

REPORT_DIR = OUTPUT_DIR / "reports"

REPORT_PATH = REPORT_DIR / "model_report.txt"

NOTEBOOK_DIR = BASE_DIR / "notebooks"

FEATURE_COLUMNS_PATH = MODEL_DIR / "feature_columns.pkl"

# ==========================
# Model Parameters
# ==========================

RANDOM_STATE = 42

TEST_SIZE = 0.20

# ==========================
# Create Required Folders
# ==========================

MODEL_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR.mkdir(parents=True, exist_ok=True)

(DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)