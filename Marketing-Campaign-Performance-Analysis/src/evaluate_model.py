import os
import joblib #type: ignore

import matplotlib.pyplot as plt
import seaborn as sns #type: ignore

import pandas as pd #type: ignore


from sklearn.metrics import ( #type: ignore

    classification_report,
    confusion_matrix,
    roc_curve,
    auc,
    accuracy_score

)


from src.preprocessing import prepare_data

from src.config import (
    MODEL_PATH,
    GRAPH_DIR,
    REPORT_DIR
)



sns.set_theme(
    style="whitegrid"
)



# ==================================
# Load Model
# ==================================

def load_model():

    model = joblib.load(
        MODEL_PATH
    )

    return model



# ==================================
# Confusion Matrix
# ==================================

def plot_confusion_matrix(
        y_test,
        predictions
):

    cm = confusion_matrix(
        y_test,
        predictions
    )


    plt.figure(
        figsize=(7,5)
    )


    sns.heatmap(

        cm,

        annot=True,

        fmt="d",

        cmap="Blues"

    )


    plt.title(
        "Confusion Matrix",
        fontsize=16,
        fontweight="bold"
    )


    plt.xlabel(
        "Predicted"
    )


    plt.ylabel(
        "Actual"
    )


    path = os.path.join(

        GRAPH_DIR,

        "confusion_matrix.png"

    )


    plt.savefig(

        path,

        dpi=300,

        bbox_inches="tight"

    )


    plt.close()



# ==================================
# ROC Curve
# ==================================

def plot_roc_curve(
        model,
        X_test,
        y_test
):


    probability = model.predict_proba(
        X_test
    )[:,1]


    fpr, tpr, threshold = roc_curve(

        y_test,

        probability

    )


    roc_auc = auc(
        fpr,
        tpr
    )


    plt.figure(
        figsize=(8,5)
    )


    plt.plot(

        fpr,

        tpr,

        label=f"AUC = {roc_auc:.3f}"

    )


    plt.plot(

        [0,1],

        [0,1]

    )


    plt.title(

        "ROC Curve",

        fontsize=16,

        fontweight="bold"

    )


    plt.xlabel(
        "False Positive Rate"
    )


    plt.ylabel(
        "True Positive Rate"
    )


    plt.legend()



    path = os.path.join(

        GRAPH_DIR,

        "roc_curve.png"

    )


    plt.savefig(

        path,

        dpi=300,

        bbox_inches="tight"

    )


    plt.close()



# ==================================
# Feature Importance
# ==================================

def feature_importance(model):

    try:

        classifier = model.named_steps["model"]

        preprocessor = model.named_steps["preprocessor"]


        # Get feature names

        feature_names = (
            preprocessor
            .get_feature_names_out()
        )


        # Random Forest / Decision Tree

        if hasattr(
            classifier,
            "feature_importances_"
        ):

            importance = classifier.feature_importances_



        # Logistic Regression

        elif hasattr(
            classifier,
            "coef_"
        ):

            importance = abs(
                classifier.coef_[0]
            )


        else:

            print(
                "Feature importance not available"
            )

            return



        feature_df = pd.DataFrame(

            {
                "Feature":
                feature_names,

                "Importance":
                importance
            }

        )


        feature_df = (
            feature_df
            .sort_values(
                by="Importance",
                ascending=False
            )
            .head(15)
        )


        plt.figure(
            figsize=(10,6)
        )


        sns.barplot(

            data=feature_df,

            x="Importance",

            y="Feature"

        )


        plt.title(
            "Top 15 Important Features",
            fontsize=16,
            fontweight="bold"
        )


        plt.xlabel(
            "Importance Score"
        )


        plt.ylabel(
            "Features"
        )


        path = os.path.join(

            GRAPH_DIR,

            "feature_importance.png"

        )


        plt.savefig(

            path,

            dpi=300,

            bbox_inches="tight"

        )


        plt.close()


        print(
            "Feature Importance Graph Saved"
        )


    except Exception as e:

        print(
            "Feature importance error:",
            e
        ) #type: ignore


# ==================================
# Evaluation Pipeline
# ==================================

def evaluate():


    print(
        "Loading Data..."
    )


    (

        X_train,

        X_test,

        y_train,

        y_test,

        preprocessor

    ) = prepare_data()



    model = load_model()



    predictions = model.predict(
        X_test
    )



    accuracy = accuracy_score(

        y_test,

        predictions

    )



    print(
        f"Accuracy: {accuracy:.4f}"
    )



    print(

        classification_report(

            y_test,

            predictions

        )

    )



    # Graphs

    plot_confusion_matrix(

        y_test,

        predictions

    )


    plot_roc_curve(

        model,

        X_test,

        y_test

    )


    feature_importance(
        model
    )



    # Save Report


    report_path = os.path.join(

        REPORT_DIR,

        "evaluation_report.txt"

    )


    with open(

        report_path,

        "w"

    ) as file:


        file.write(

            classification_report(

                y_test,

                predictions

            )

        )


    print(
        "Evaluation Completed"
    )



if __name__ == "__main__":

    evaluate()