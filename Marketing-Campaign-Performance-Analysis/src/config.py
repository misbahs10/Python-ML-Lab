import os


# ==============================
# PROJECT ROOT
# ==============================

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ==============================
# DATA PATHS
# ==============================

DATA_DIR = os.path.join(
    ROOT_DIR,
    "data"
)


RAW_DATA_PATH = os.path.join(
    DATA_DIR,
    "raw",
    "marketing_campaign.csv"
)


PROCESSED_DATA_PATH = os.path.join(
    DATA_DIR,
    "processed",
    "cleaned_campaign_data.csv"
)



# ==============================
# MODEL PATH
# ==============================

MODEL_DIR = os.path.join(
    ROOT_DIR,
    "models"
)


MODEL_PATH = os.path.join(
    MODEL_DIR,
    "campaign_model.pkl"
)



# ==============================
# OUTPUT PATHS
# ==============================

OUTPUT_DIR = os.path.join(
    ROOT_DIR,
    "outputs"
)


GRAPH_DIR = os.path.join(
    OUTPUT_DIR,
    "graphs"
)


REPORT_DIR = os.path.join(
    OUTPUT_DIR,
    "reports"
)



# ==============================
# CREATE DIRECTORIES
# ==============================

directories = [

    DATA_DIR,
    os.path.join(DATA_DIR,"processed"),
    MODEL_DIR,
    GRAPH_DIR,
    REPORT_DIR

]


for directory in directories:

    os.makedirs(
        directory,
        exist_ok=True
    )



# ==============================
# ML SETTINGS
# ==============================

RANDOM_STATE = 42

TEST_SIZE = 0.20