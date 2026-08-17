# NEW ###########################
import streamlit as st
from datetime import datetime
import requests

BACKEND_URL = "https://superkart-backend-rwmz.onrender.com"

# Wake up the backend as soon as the page loads (once per session)
if "backend_warmed" not in st.session_state:
    with st.spinner("Waking up the prediction service... this can take up to a minute on first load"):
        try:
            requests.get(BACKEND_URL, timeout=90)
            st.session_state["backend_warmed"] = True
        except requests.exceptions.RequestException:
            st.session_state["backend_warmed"] = False

st.subheader("SuperKart Retail Sales Forecasting Dashboard")
st.write(f"Current date&time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.slider("Product Allocated Area Ratio", min_value=0.000, max_value=1.000, value=0.066, step=0.001, format="%.3f")
Product_MRP = st.number_input("Product Maximum Retail Price (\u20b9)", min_value=0.0, max_value=500.0, value=141.0, step=0.5)
Store_Size = st.selectbox("Store Size Tier", ["High", "Medium", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Class", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Format Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])
Product_Id_char = st.selectbox("Product Category Code", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Operational Age (Years)", min_value=0, max_value=100, value=15, step=1)
Product_Type_Category = st.selectbox("Product Category", ["Perishables", "Non Perishables"])

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

if st.button("Predict", type='primary'):
    with st.spinner("Getting prediction..."):
        try:
            response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data, timeout=90)
            if response.status_code == 200:
                result = response.json()
                predicted_sales = result["Sales"]
                st.success(f"Predicted Product Store Sales Total: \u20b9{predicted_sales:,.2f}")
            else:
                st.error(f"Error in API request (status {response.status_code})")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach the backend: {e}")
