import pandas as pd #type: ignore

from sklearn.model_selection import train_test_split #type: ignore

from sklearn.preprocessing import ( #type: ignore
    StandardScaler,
    OneHotEncoder
)

from sklearn.compose import ColumnTransformer #type: ignore

from sklearn.pipeline import Pipeline #type: ignore

from sklearn.impute import SimpleImputer #type: ignore

import joblib #type: ignore


from src.config import (
    PROCESSED_DATA_PATH,
    MODEL_DIR,
    RANDOM_STATE,
    TEST_SIZE
)



# ==================================
# Feature Engineering
# ==================================

def create_features(df):


    # Customer Age

    df["age"] = (
        2026 - df["year_birth"]
    )


    # Total Spending

    spending_columns = [

        "mntwines",
        "mntfruits",
        "mntmeatproducts",
        "mntfishproducts",
        "mntsweetproducts",
        "mntgoldprods"

    ]


    df["total_spending"] = (
        df[spending_columns]
        .sum(axis=1)
    )



    # Total Purchases

    purchase_columns = [

        "numwebpurchases",
        "numcatalogpurchases",
        "numstorepurchases"

    ]


    df["total_purchases"] = (
        df[purchase_columns]
        .sum(axis=1)
    )


    return df



# ==================================
# Prepare Dataset
# ==================================

def prepare_data():

    print(
        "Loading Clean Dataset..."
    )


    df = pd.read_csv(
        PROCESSED_DATA_PATH
    )


    print(
        "Original Shape:",
        df.shape
    )


    # Feature Creation

    df = create_features(df)



    # Remove unnecessary columns

    drop_columns = [

        "id",
        "year_birth",
        "dt_customer"

    ]


    df.drop(
        columns=drop_columns,
        inplace=True,
        errors="ignore"
    )



    # Target

    X = df.drop(
        "response",
        axis=1
    )


    y = df["response"]



    # Identify Columns

    categorical_columns = (
        X.select_dtypes(
            include="object"
        )
        .columns
        .tolist()
    )


    numerical_columns = (
        X.select_dtypes(
            include=["int64","float64"]
        )
        .columns
        .tolist()
    )



    print(
        "Categorical Features:",
        categorical_columns
    )


    print(
        "Numerical Features:",
        numerical_columns
    )



    # Preprocessing Pipeline


    numerical_pipeline = Pipeline(

        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            ),

            (
                "scaler",
                StandardScaler()
            )

        ]

    )



    categorical_pipeline = Pipeline(

        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )

        ]

    )



    preprocessor = ColumnTransformer(

        transformers=[

            (
                "num",
                numerical_pipeline,
                numerical_columns
            ),


            (
                "cat",
                categorical_pipeline,
                categorical_columns
            )

        ]

    )



    # Train Test Split


    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=TEST_SIZE,

        random_state=RANDOM_STATE,

        stratify=y

    )



    print(
        "Training Data:",
        X_train.shape
    )


    print(
        "Testing Data:",
        X_test.shape
    )



    return (

        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor

    )



if __name__ == "__main__":


    prepare_data()