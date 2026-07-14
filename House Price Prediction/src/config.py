import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Folders
DATA_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_DIR = os.path.join(BASE_DIR, "models")
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# File Paths
DATA_PATH = os.path.join(DATA_DIR, "Housing.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "house_price_model.pkl")

# ML Parameters
TEST_SIZE = 0.20
RANDOM_STATE = 42