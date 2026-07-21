import pandas as pd # type:ignore
import joblib # type:ignore

from sklearn.model_selection import train_test_split # type:ignore
from sklearn.preprocessing import StandardScaler # type:ignore

from config import (
    DATA_PATH,
    RANDOM_STATE,
    TEST_SIZE,
    FEATURE_COLUMNS_PATH,
    X_TRAIN_PATH,
    X_TEST_PATH,
    Y_TRAIN_PATH,
    Y_TEST_PATH,
    SCALER_PATH,
)

from utils import print_title, dataset_summary


# ==========================================
# Load Dataset
# ==========================================

print_title("Loading Dataset")

data = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully")

dataset_summary(data)

# ==========================================
# Remove Duplicate Records
# ==========================================

print_title("Removing Duplicates")

duplicates = data.duplicated().sum()

print("Duplicate Rows :", duplicates)

data = data.drop_duplicates()

print("Remaining Rows :", len(data))

# ==========================================
# Encode Target Variable
# ==========================================

print_title("Encoding Target")

data["Attrition"] = data["Attrition"].map(
    {
        "No": 0,
        "Yes": 1,
    }
)

# ==========================================
# One Hot Encoding
# ==========================================

print_title("Encoding Categorical Features")

categorical_columns = data.select_dtypes(include="object").columns

data = pd.get_dummies(
    data,
    columns=categorical_columns,
    drop_first=True,
)

print("Encoding Completed")

# ==========================================
# Split Features & Target
# ==========================================

print_title("Splitting Dataset")

X = data.drop("Attrition", axis=1)

y = data["Attrition"]

print("Features :", X.shape)

print("Target :", y.shape)

# ==========================================
# Train Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)

print("Training Shape :", X_train.shape)

print("Testing Shape :", X_test.shape)

feature_columns = X.columns.tolist()

joblib.dump(feature_columns, FEATURE_COLUMNS_PATH)

# ==========================================
# Feature Scaling
# ==========================================

print_title("Scaling Features")

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

joblib.dump(scaler, SCALER_PATH)

print("Scaler Saved Successfully")

# ==========================================
# Convert Back to DataFrame
# ==========================================

X_train = pd.DataFrame(
    X_train,
    columns=X.columns,
)

X_test = pd.DataFrame(
    X_test,
    columns=X.columns,
)

# ==========================================
# Save Processed Data
# ==========================================

print_title("Saving Processed Dataset")

X_train.to_csv(X_TRAIN_PATH, index=False)

X_test.to_csv(X_TEST_PATH, index=False)

pd.DataFrame(y_train).to_csv(Y_TRAIN_PATH, index=False)

pd.DataFrame(y_test).to_csv(Y_TEST_PATH, index=False)

print("Files Saved Successfully")

print("\n✔ X_train.csv")
print("✔ X_test.csv")
print("✔ y_train.csv")
print("✔ y_test.csv")

print_title("Data Preprocessing Completed Successfully")