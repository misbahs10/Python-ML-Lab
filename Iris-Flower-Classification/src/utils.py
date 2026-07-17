import joblib # type: ignore


def load_model(model_path):
    """
    Load trained model.
    """
    try:
        model = joblib.load(model_path)
        return model

    except FileNotFoundError:
        print("\nModel file not found.")
        print("Run train_model.py first.")
        exit()

    except Exception as e:
        print("\nError loading model:")
        print(e)
        exit()


def get_float_input(message):
    """
    Get validated float input from user.
    """

    while True:

        try:

            value = float(input(message))

            if value < 0:
                print("Value cannot be negative.\n")
                continue

            return value

        except ValueError:

            print("Please enter a valid numeric value.\n")