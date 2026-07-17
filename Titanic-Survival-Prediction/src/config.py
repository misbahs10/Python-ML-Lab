import os

# Project Root Folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset Path
DATA_PATH = os.path.join(BASE_DIR, "data", "Titanic-Dataset.csv")

# Model Save Path
MODEL_PATH = os.path.join(BASE_DIR, "models", "titanic_model.pkl")