import streamlit as st

from src.predict import predict_campaign



# ==================================
# Page Configuration
# ==================================

st.set_page_config(

    page_title="Marketing Campaign AI",

    page_icon="📊",

    layout="wide"

)



# ==================================
# Title
# ==================================

st.title(
    "📊 Marketing Campaign Performance Prediction"
)


st.write(
    """
    This AI application predicts whether a customer
    will accept a marketing campaign or not.
    """
)



st.divider()



# ==================================
# Customer Input Section
# ==================================

st.subheader(
    "Customer Information"
)



col1, col2, col3 = st.columns(3)



with col1:


    year_birth = st.number_input(

        "Birth Year",

        min_value=1940,

        max_value=2020,

        value=1985

    )


    education = st.selectbox(

        "Education",

        [

            "Graduation",

            "PhD",

            "Master",

            "Basic"

        ]

    )


    marital_status = st.selectbox(

        "Marital Status",

        [

            "Married",

            "Single",

            "Divorced",

            "Together"

        ]

    )


    income = st.number_input(

        "Income",

        value=60000

    )



with col2:


    kidhome = st.number_input(

        "Kids at Home",

        min_value=0,

        value=0

    )


    teenhome = st.number_input(

        "Teenagers at Home",

        min_value=0,

        value=1

    )


    recency = st.number_input(

        "Days Since Last Purchase",

        value=20

    )


    country = st.selectbox(

        "Country",

        [

            "Spain",

            "India",

            "Germany",

            "France",

            "Pakistan"

        ]

    )



with col3:


    mntwines = st.number_input(

        "Wine Spending",

        value=500

    )


    mntfruits = st.number_input(

        "Fruit Spending",

        value=50

    )


    mntmeatproducts = st.number_input(

        "Meat Spending",

        value=300

    )


    mntfishproducts = st.number_input(

        "Fish Spending",

        value=40

    )



st.divider()



# ==================================
# Purchase Information
# ==================================

st.subheader(
    "Purchase Behaviour"
)



col4, col5, col6 = st.columns(3)



with col4:


    mntsweetproducts = st.number_input(

        "Sweet Products",

        value=30

    )


    mntgoldprods = st.number_input(

        "Gold Products",

        value=20

    )



with col5:


    numwebpurchases = st.number_input(

        "Web Purchases",

        value=5

    )


    numcatalogpurchases = st.number_input(

        "Catalog Purchases",

        value=3

    )



with col6:


    numstorepurchases = st.number_input(

        "Store Purchases",

        value=6

    )


    numwebvisitsmonth = st.number_input(

        "Website Visits",

        value=5

    )



# Campaign History

acceptedcmp1 = 0
acceptedcmp2 = 0
acceptedcmp3 = 0
acceptedcmp4 = 0
acceptedcmp5 = 0

complain = 0



st.divider()



# ==================================
# Prediction Button
# ==================================

if st.button(

    "🚀 Predict Campaign Response",

    use_container_width=True

):


    customer = {


        "year_birth": year_birth,


        "education": education,


        "marital_status": marital_status,


        "income": income,


        "kidhome": kidhome,


        "teenhome": teenhome,


        "recency": recency,


        "mntwines": mntwines,


        "mntfruits": mntfruits,


        "mntmeatproducts": mntmeatproducts,


        "mntfishproducts": mntfishproducts,


        "mntsweetproducts": mntsweetproducts,


        "mntgoldprods": mntgoldprods,


        "numdealspurchases": 2,


        "numwebpurchases": numwebpurchases,


        "numcatalogpurchases": numcatalogpurchases,


        "numstorepurchases": numstorepurchases,


        "numwebvisitsmonth": numwebvisitsmonth,


        "acceptedcmp1": acceptedcmp1,


        "acceptedcmp2": acceptedcmp2,


        "acceptedcmp3": acceptedcmp3,


        "acceptedcmp4": acceptedcmp4,


        "acceptedcmp5": acceptedcmp5,


        "complain": complain,


        "country": country

    }



    result = predict_campaign(
        customer
    )



    st.success(
        "Prediction Completed!"
    )



    col7, col8 = st.columns(2)



    with col7:

        st.metric(

            "Prediction",

            result["Prediction"]

        )



    with col8:

        st.metric(

            "Success Probability",

            result["Success Probability"]

        )



    if "Accepted" in result["Prediction"]:

        st.balloons()

        st.info(

            "This customer is likely to respond positively."

        )


    else:

        st.warning(

            "This customer has a low campaign response probability."

        )



# ==================================
# Footer
# ==================================

st.divider()


st.caption(

    "Built with Python | Machine Learning | Streamlit"

)