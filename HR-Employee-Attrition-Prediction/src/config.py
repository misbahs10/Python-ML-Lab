from pathlib import Path

# ==========================================================
# Base Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "reports"

# ==========================================================
# Files
# ==========================================================

DATA_PATH = DATA_DIR / "HR_Employee_Attrition.csv"

MODEL_PATH = MODEL_DIR / "employee_attrition_model.pkl"

SCALER_PATH = MODEL_DIR / "scaler.pkl"

FEATURE_COLUMNS_PATH = MODEL_DIR / "feature_columns.pkl"

# ==========================================================
# Random State
# ==========================================================

RANDOM_STATE = 42

# ==========================================================
# Test Size
# ==========================================================

TEST_SIZE = 0.20

# ==========================================================
# Create Missing Directories
# ==========================================================

MODEL_DIR.mkdir(exist_ok=True)

REPORT_DIR.mkdir(exist_ok=True)

# ==========================================
# Processed Dataset
# ==========================================

X_TRAIN_PATH = DATA_DIR / "X_train.csv"
X_TEST_PATH = DATA_DIR / "X_test.csv"

Y_TRAIN_PATH = DATA_DIR / "y_train.csv"
Y_TEST_PATH = DATA_DIR / "y_test.csv"