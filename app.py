# NEW ###########################
import streamlit as st
import requests

st.title("SuperKart Retail Sales Forecasting Dashboard")

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
    response = requests.post("https://lupper-superkart-backend.onrender.com/v1/predict", json=product_data)
    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Sales"]
        st.write(f"Predicted Product Store Sales Total: \u20b9{predicted_sales:.2f}")
    else:
        st.error("Error in API request")
