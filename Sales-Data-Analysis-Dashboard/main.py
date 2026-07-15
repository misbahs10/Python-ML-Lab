from src.data_preprocessing import preprocess_data
from src.analysis import sales_analysis
from src.dashboard import create_dashboard
from src.business_analysis import business_analysis
from src.advanced_analysis import advanced_analysis

print("=" * 60)
print(" SALES DATA ANALYSIS DASHBOARD ")
print("=" * 60)

data = preprocess_data()

if data is not None:
    sales_analysis(data)
    create_dashboard(data)
    business_analysis(data)
    advanced_analysis(data)

print("\nProject Completed Successfully.")