"""
============================================
Sales Data Analysis Dashboard
Configuration File
============================================
"""

import os

# Project Root Folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset Path
DATA_PATH = os.path.join(BASE_DIR, "data", "Sample - Superstore.csv")

# Output Folder
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Automatically create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)