import joblib # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.tree import DecisionTreeClassifier # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore

from sklearn.metrics import ( # type: ignore
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_curve,
    roc_auc_score
)

from config import (
    X_TRAIN_PATH,
    X_TEST_PATH,
    Y_TRAIN_PATH,
    Y_TEST_PATH,
    MODEL_PATH,
    REPORT_DIR,
    RANDOM_STATE
)

from utils import print_title

print_title("Loading Processed Dataset")

X_train = pd.read_csv(X_TRAIN_PATH)
X_test = pd.read_csv(X_TEST_PATH)

y_train = pd.read_csv(Y_TRAIN_PATH).values.ravel()
y_test = pd.read_csv(Y_TEST_PATH).values.ravel()

models = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Decision Tree":
        DecisionTreeClassifier(random_state=RANDOM_STATE),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=200,
            random_state=RANDOM_STATE
        )

}

results = {}

best_model = None

best_accuracy = 0

for name, model in models.items():

    print_title(name)

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)

    precision = precision_score(y_test, prediction)

    recall = recall_score(y_test, prediction)

    f1 = f1_score(y_test, prediction)

    results[name] = accuracy

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    print("\nClassification Report\n")

    print(classification_report(y_test, prediction))

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model

joblib.dump(best_model, MODEL_PATH)

print_title("Best Model Saved Successfully")

prediction = best_model.predict(X_test)

cm = confusion_matrix(y_test, prediction)

plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Confusion Matrix")

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(
    REPORT_DIR/"confusion_matrix.png",
    dpi=300
)

plt.show()

probability = best_model.predict_proba(X_test)[:,1]

fpr, tpr, _ = roc_curve(
    y_test,
    probability
)

auc = roc_auc_score(
    y_test,
    probability
)

plt.figure(figsize=(8,6))

plt.plot(
    fpr,
    tpr,
    label=f"AUC = {auc:.3f}",
    linewidth=3
)

plt.plot(
    [0,1],
    [0,1],
    linestyle="--"
)

plt.legend()

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title("ROC Curve")

plt.tight_layout()

plt.savefig(
    REPORT_DIR/"roc_curve.png",
    dpi=300
)

plt.show()

if hasattr(best_model,"feature_importances_"):

    importance = pd.Series(

        best_model.feature_importances_,
        index=X_train.columns

    )

    importance = importance.sort_values(
        ascending=False
    )[:15]

    plt.figure(figsize=(10,7))

    sns.barplot(

        x=importance.values,
        y=importance.index

    )

    plt.title("Top 15 Important Features")

    plt.tight_layout()

    plt.savefig(
        REPORT_DIR/"feature_importance.png",
        dpi=300
    )

    plt.show()

plt.figure(figsize=(8,5))

sns.barplot(

    x=list(results.keys()),
    y=list(results.values())

)

plt.title("Model Accuracy Comparison")

plt.ylabel("Accuracy")

plt.tight_layout()

plt.savefig(
    REPORT_DIR/"model_comparison.png",
    dpi=300
)

plt.show()

print_title("Training Completed")

print("Best Accuracy :", best_accuracy)

print("Model Saved Successfully")