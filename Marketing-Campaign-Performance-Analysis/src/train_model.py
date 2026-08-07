import joblib #type: ignore
import os

from sklearn.pipeline import Pipeline #type: ignore

from sklearn.linear_model import LogisticRegression #type: ignore

from sklearn.tree import DecisionTreeClassifier #type: ignore

from sklearn.ensemble import RandomForestClassifier #type: ignore


from sklearn.metrics import ( #type: ignore
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


from src.preprocessing import prepare_data

from src.config import (
    MODEL_PATH,
    REPORT_DIR
)



# ==================================
# Train Models
# ==================================

def train_models():


    print(
        "Preparing Data..."
    )


    (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor

    ) = prepare_data()



    models = {


        "Logistic Regression":

        LogisticRegression(
            max_iter=1000
        ),



        "Decision Tree":

        DecisionTreeClassifier(
            random_state=42
        ),



        "Random Forest":

        RandomForestClassifier(

            n_estimators=200,

            random_state=42

        )

    }



    results = {}

    best_model = None

    best_score = 0



    for name, model in models.items():


        print(
            f"\nTraining {name}..."
        )


        pipeline = Pipeline(

            steps=[

                (
                    "preprocessor",
                    preprocessor
                ),


                (
                    "model",
                    model
                )

            ]

        )



        pipeline.fit(
            X_train,
            y_train
        )



        predictions = pipeline.predict(
            X_test
        )



        accuracy = accuracy_score(
            y_test,
            predictions
        )


        precision = precision_score(
            y_test,
            predictions
        )


        recall = recall_score(
            y_test,
            predictions
        )


        f1 = f1_score(
            y_test,
            predictions
        )



        results[name] = {


            "Accuracy":
            accuracy,


            "Precision":
            precision,


            "Recall":
            recall,


            "F1 Score":
            f1

        }



        print(
            f"{name} Accuracy: {accuracy:.4f}"
        )



        if accuracy > best_score:

            best_score = accuracy

            best_model = pipeline



    # Save Best Model


    joblib.dump(

        best_model,

        MODEL_PATH

    )



    print(
        "\nBest Model Saved:"
    )


    print(
        MODEL_PATH
    )



    # Save Report


    report_path = os.path.join(

        REPORT_DIR,

        "model_report.txt"

    )



    with open(
        report_path,
        "w"
    ) as file:


        file.write(
            "Marketing Campaign Model Report\n"
        )


        file.write(
            "="*40 + "\n\n"
        )



        for model, metrics in results.items():

            file.write(
                f"{model}\n"
            )


            for metric,value in metrics.items():

                file.write(
                    f"{metric}: {value:.4f}\n"
                )


            file.write(
                "\n"
            )



    print(
        "Report Saved Successfully"
    )



if __name__ == "__main__":

    train_models()