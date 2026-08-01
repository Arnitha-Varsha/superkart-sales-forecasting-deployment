import streamlit as st
import requests
import pandas as pd

st.title("SuperKart Sales Forecasting")

st.write("""
### Predict the total sales for a product at a specific store.
Enter the product and store details below.
""")

# Input fields for the features
product_weight = st.number_input("Product Weight", min_value=0.0, value=12.0)
product_sugar = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
allocated_area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.06)
product_type = st.selectbox("Product Type", ["Frozen Foods", "Dairy", "Canned", "Baking Goods", "Health and Hygiene", "Meat", "Snack Foods", "Hard Drinks", "Soft Drinks", "Bread", "Breakfast", "Fruits and Vegetables", "Household", "Seafood", "Starchy foods", "Others"])
mrp = st.number_input("Product MRP", min_value=0.0, value=140.0)
store_size = st.selectbox("Store Size", ["High", "Medium", "Small"])
city_type = st.selectbox("City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])
store_age = st.number_input("Store Age (Years)", min_value=0, value=15)

# Backend URL - this will be used when running containers in a network
backend_url = "http://superkart-backend:7860/v1/predict"

if st.button("Predict Sales"):
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar,
        "Product_Allocated_Area": allocated_area,
        "Product_Type": product_type,
        "Product_MRP": mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": city_type,
        "Store_Type": store_type,
        "Store_Age": store_age
    }
    
    try:
        response = requests.post(backend_url, json=payload)
        if response.status_code == 200:
            prediction = response.json().get('Predicted_Product_Store_Sales_Total', 0)
            st.success(f"Predicted Total Sales: ${prediction:,.2f}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")
