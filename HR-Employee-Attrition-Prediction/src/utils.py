import pandas as pd # type:ignore


def print_title(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def dataset_summary(data):

    print_title("Dataset Information")

    print(f"Rows    : {data.shape[0]}")
    print(f"Columns : {data.shape[1]}")

    print("\nData Types\n")
    print(data.dtypes)

    print("\nMissing Values\n")
    print(data.isnull().sum())

    print("\nDuplicate Rows :", data.duplicated().sum())