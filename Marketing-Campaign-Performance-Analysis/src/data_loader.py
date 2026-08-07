import pandas as pd #type: ignore

from src.config import RAW_DATA_PATH



def load_data():

    df = pd.read_csv(
        RAW_DATA_PATH
    )

    return df



def dataset_information(df):

    print("\nDataset Shape:")
    print(df.shape)


    print("\nColumns:")
    print(df.columns.tolist())


    print("\nMissing Values:")
    print(df.isnull().sum())



if __name__ == "__main__":

    data = load_data()


    print(
        "Dataset Loaded Successfully"
    )


    dataset_information(data)


    print(
        "\nFirst 5 Rows:"
    )

    print(
        data.head()
    )