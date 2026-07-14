import os
import joblib  # type: ignore
from typing import Any


def create_directory(path: str) -> None:
    """
    Create directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)


def save_model(model: Any, path: str) -> None:
    """
    Save trained model.
    """
    joblib.dump(model, path)
    print(f"\n✅ Model saved at:\n{path}")
    

def load_model(path: str) -> Any:
    """Load saved model."""
    return joblib.load(path)