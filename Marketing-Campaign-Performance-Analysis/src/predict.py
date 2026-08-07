import pandas as pd #type: ignore
import joblib #type: ignore

from src.config import MODEL_PATH



# ==================================
# Load Trained Model
# ==================================

def load_model():

    model = joblib.load(
        MODEL_PATH
    )

    return model



# ==================================
# Feature Engineering
# ==================================

def create_features(data):


    # Create Age Feature

    if "year_birth" in data.columns:

        data["age"] = (
            2026 - data["year_birth"]
        )

    else:

        data["age"] = 40



    # Total Spending Feature

    spending_columns = [

        "mntwines",
        "mntfruits",
        "mntmeatproducts",
        "mntfishproducts",
        "mntsweetproducts",
        "mntgoldprods"

    ]


    data["total_spending"] = (
        data[spending_columns]
        .sum(axis=1)
    )



    # Total Purchases Feature

    purchase_columns = [

        "numwebpurchases",
        "numcatalogpurchases",
        "numstorepurchases"

    ]


    data["total_purchases"] = (

        data[purchase_columns]
        .sum(axis=1)

    )



    # Remove unnecessary columns

    data.drop(

        columns=[

            "id",
            "year_birth",
            "dt_customer"

        ],

        inplace=True,

        errors="ignore"

    )


    return data




# ==================================
# Prediction Function
# ==================================

def predict_campaign(customer_data):


    model = load_model()



    df = pd.DataFrame(
        [customer_data]
    )



    df = create_features(
        df
    )



    prediction = model.predict(
        df
    )



    probability = model.predict_proba(
        df
    )



    result = {


        "Prediction":

        (

            "Campaign Accepted"

            if prediction[0] == 1

            else

            "Campaign Rejected"

        ),



        "Success Probability":

        round(

            probability[0][1] * 100,

            2

        )

    }



    return result




# ==================================
# Testing
# ==================================

if __name__ == "__main__":


    sample_customer = {


        "year_birth": 1985,


        "education":

        "Graduation",



        "marital_status":

        "Married",



        "income":

        60000,



        "kidhome":

        0,



        "teenhome":

        1,



        "recency":

        20,



        "mntwines":

        500,



        "mntfruits":

        50,



        "mntmeatproducts":

        300,



        "mntfishproducts":

        40,



        "mntsweetproducts":

        30,



        "mntgoldprods":

        20,



        "numdealspurchases":

        2,



        "numwebpurchases":

        5,



        "numcatalogpurchases":

        3,



        "numstorepurchases":

        6,



        "numwebvisitsmonth":

        5,



        "acceptedcmp1":

        0,



        "acceptedcmp2":

        0,



        "acceptedcmp3":

        0,



        "acceptedcmp4":

        0,



        "acceptedcmp5":

        0,



        "complain":

        0,



        "country":

        "Spain"

    }



    result = predict_campaign(
        sample_customer
    )



    print("\nPrediction Result")
    print("------------------")

    print(result)