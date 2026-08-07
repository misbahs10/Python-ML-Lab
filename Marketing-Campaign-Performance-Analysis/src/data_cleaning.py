import pandas as pd #type: ignore

from src.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH
)



def load_raw_data():

    df = pd.read_csv(
        RAW_DATA_PATH,
    )

    return df



# ==============================
# Missing Values
# ==============================

def check_missing_values(df):

    print("\nMissing Values:")
    
    print(
        df.isnull()
        .sum()
    )



# ==============================
# Duplicate Removal
# ==============================

def remove_duplicates(df):

    before = df.shape[0]


    df = df.drop_duplicates()


    after = df.shape[0]


    print(
        f"\nRemoved Duplicates: {before-after}"
    )


    return df



# ==============================
# Column Cleaning
# ==============================

def clean_columns(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ","_")
    )


    return df



# ==============================
# Income Cleaning
# ==============================

def clean_income(df):

    if "income" in df.columns:

        df["income"] = (
            df["income"]
            .fillna(
                df["income"].median()
            )
        )


    return df



# ==============================
# Full Pipeline
# ==============================

def clean_data():

    print(
        "Loading Dataset..."
    )


    df = load_raw_data()


    print(
        "Original Shape:",
        df.shape
    )


    check_missing_values(df)


    df = remove_duplicates(df)


    df = clean_columns(df)


    df = clean_income(df)



    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )


    print(
        "\nCleaning Completed"
    )


    print(
        "Final Shape:",
        df.shape
    )


    print(
        "\nSaved File:"
    )

    print(
        PROCESSED_DATA_PATH
    )



if __name__ == "__main__":

    clean_data()