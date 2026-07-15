"""
============================================
Sales Data Analysis Dashboard
Utility Functions
============================================
"""

import pandas as pd # type: ignore


def load_data(file_path):
    """
    Load CSV dataset
    """
    try:
        data = pd.read_csv(file_path, encoding="latin1")
        print("Dataset Loaded Successfully.")
        return data

    except FileNotFoundError:
        print("Dataset file not found.")
        return None

    except Exception as e:
        print("Error:", e)
        return None