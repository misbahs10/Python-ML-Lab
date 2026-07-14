from src.predict import predict_price


def menu():

    while True:

        print("\n==============================")
        print(" House Price Prediction ")
        print("==============================")
        print("1. Predict House Price")
        print("2. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            predict_price()

        elif choice == "2":
            print("\nThank you 😊")
            break

        else:
            print("\nInvalid Choice")


if __name__ == "__main__":
    menu()