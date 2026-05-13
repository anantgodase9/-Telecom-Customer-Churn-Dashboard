import streamlit as st
import json
import pandas as pd
import xgboost as xgb

st.set_page_config(page_title="Churn Predictor", layout="wide")

# Load feature names
with open('model/feature_names.json') as f:
    feature_names = json.load(f)

# Load XGBoost Booster model
model = xgb.Booster()
model.load_model('model/churn_model.json')

st.markdown("<h1 style='text-align: center;'>📊 Customer Churn Prediction</h1>", unsafe_allow_html=True)

st.write("""
This app predicts **customer churn** based on input features.  
Adjust the features below and see the predicted risk!
""")

st.sidebar.header("Customer Information")

# Numerical features
tenure = st.sidebar.slider('Tenure (months)', 0, 72, 12)
# Monthly Charges
monthly_charges_usd = st.sidebar.slider('Monthly Charges (USD)', 18, 120, 70)
monthly_charges = monthly_charges_usd   # ✅ THIS LINE IS IMPORTANT
st.sidebar.write(f"₹ {monthly_charges_usd * 83:.0f}")

# Total Charges
total_charges_usd = st.sidebar.slider('Total Charges (USD)', 0, 9000, 1000)
total_charges = total_charges_usd   # ✅ THIS LINE IS IMPORTANT
st.sidebar.write(f"₹ {total_charges_usd * 83:.0f}")
# Contract type
contract = st.sidebar.selectbox("Contract Type", ("Month-to-month", "One year", "Two year"))

# Internet service
internet_service = st.sidebar.selectbox("Internet Service", ("Fiber optic", "DSL", "No"))

# Online security
online_security = st.sidebar.selectbox("Online Security", ("Yes", "No"))

# Tech support
tech_support = st.sidebar.selectbox("Tech Support", ("Yes", "No"))

# Payment method
payment_method = st.sidebar.selectbox("Payment Method", ("Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"))

# Base numeric features
input_data = {
    'tenure': tenure,
    'MonthlyCharges': monthly_charges,
    'TotalCharges': total_charges,
    'gender': 1,  # default example (could be extended)
    'SeniorCitizen': 0,
    'Partner': 1,
    'Dependents': 0,
    'PhoneService': 1,
    'PaperlessBilling': 1,
}

# One-hot features
input_data['Contract_Month-to-month'] = 1 if contract == "Month-to-month" else 0
input_data['Contract_One year'] = 1 if contract == "One year" else 0
input_data['Contract_Two year'] = 1 if contract == "Two year" else 0

input_data['InternetService_Fiber optic'] = 1 if internet_service == "Fiber optic" else 0
input_data['InternetService_DSL'] = 1 if internet_service == "DSL" else 0
input_data['InternetService_No'] = 1 if internet_service == "No" else 0

input_data['OnlineSecurity_Yes'] = 1 if online_security == "Yes" else 0
input_data['OnlineSecurity_No'] = 1 if online_security == "No" else 0

input_data['TechSupport_Yes'] = 1 if tech_support == "Yes" else 0
input_data['TechSupport_No'] = 1 if tech_support == "No" else 0

input_data['PaymentMethod_Electronic check'] = 1 if payment_method == "Electronic check" else 0
input_data['PaymentMethod_Mailed check'] = 1 if payment_method == "Mailed check" else 0
input_data['PaymentMethod_Bank transfer (automatic)'] = 1 if payment_method == "Bank transfer (automatic)" else 0
input_data['PaymentMethod_Credit card (automatic)'] = 1 if payment_method == "Credit card (automatic)" else 0

# Fill remaining columns as 0 if needed
for col in feature_names:
    if col not in input_data:
        input_data[col] = 0

# Convert to DataFrame with correct feature order
input_df_pd = pd.DataFrame([input_data])[feature_names]

# Convert to DMatrix
dtest = xgb.DMatrix(input_df_pd)

# Predict churn probability
churn_prob = model.predict(dtest)[0]

tab1, tab2 = st.tabs(["📊 Prediction", "📈 Insights"])

# Display prediction
with tab1:
    st.subheader("Predicted Churn Probability")
    st.write(f"**{churn_prob:.2%} chance this customer will churn.**")
    st.progress(int(churn_prob * 100))

    if churn_prob > 0.6:
        st.error("⚠️ High churn risk — consider immediate retention actions.")
    elif churn_prob > 0.3:
        st.warning("🟠 Medium risk — consider engagement strategies.")
    else:
        st.success("✅ Low churn risk.")

with tab2:
    st.subheader("🔍 Key Insights")

    if monthly_charges > 70:
        st.write("👉 High monthly charges increase churn risk")

    if contract == "Month-to-month":
        st.write("👉 Month-to-month contracts have higher churn")

    if tenure < 6:
        st.write("👉 New customers are more likely to churn")


    st.subheader("💡 Recommended Actions")

    if churn_prob > 0.6:
        st.write("🔴 High Risk Customer")
        if contract == "Month-to-month":
            st.write("👉 Offer discount for long-term contract")
        if monthly_charges > 70:
            st.write("👉 Provide cheaper plan or bundle offer")
        if tenure < 6:
            st.write("👉 Provide onboarding support")
        st.write("👉 Improve customer support and engagement")

    elif churn_prob > 0.3:
        st.write("🟠 Medium Risk Customer")
        st.write("👉 Offer loyalty rewards")
        st.write("👉 Send personalized offers")
        st.write("👉 Improve engagement")

    else:
        st.write("🟢 Low Risk Customer")
        st.write("👉 Upsell premium services")
        st.write("👉 Offer add-ons")


    # ✅ MOVE INSIDE TAB
    st.subheader("📌 Customer Summary")

    st.write(f"""
    - Tenure: {tenure} months  
    - Monthly Charges: ₹{monthly_charges * 83:.0f}  
    - Total Charges: ₹{total_charges * 83:.0f}  
    - Contract Type: {contract}  
    - Internet Service: {internet_service}  
    """)