import joblib # type: ignore
from sklearn.metrics import accuracy_score # type: ignore


def save_model(model, model_path):
    """
    Save trained model
    """
    joblib.dump(model, model_path)
    print(f"\nModel saved successfully at:\n{model_path}")


def load_model(model_path):
    """
    Load trained model
    """
    return joblib.load(model_path)


def calculate_accuracy(y_true, y_pred):
    """
    Calculate Accuracy
    """
    return accuracy_score(y_true, y_pred)