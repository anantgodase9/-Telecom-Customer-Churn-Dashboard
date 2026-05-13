import streamlit as st
import json
import pandas as pd
import xgboost as xgb

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Telecom Churn Dashboard",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

            /* ---------------- REVIEW SECTION ---------------- */

.review-card {
    background: rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 25px;
    margin-top: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.08);
}

/* Text Area */
textarea {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #374151 !important;
}

/* Slider */
.stSlider > div > div {
    color: #22c55e !important;
}

/* Submit Button */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    font-size: 16px;
    font-weight: bold;
    background: linear-gradient(90deg, #22c55e, #4ade80);
    color: black;
    border: none;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #16a34a, #22c55e);
}

/* Review Display Box */
.review-box {
    background: rgba(255,255,255,0.04);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    border-left: 4px solid #22c55e;
}

/* Review Title */
.review-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
    color: #4ade80;
}
            
            h
/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #020617);
}

/* Card */
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

/* Headings */
h1, h2, h3 {
    color: #e5e7eb;
}

/* Progress bar */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #22c55e, #facc15, #ef4444);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
with open('model/feature_names.json') as f:
    feature_names = json.load(f)

model = xgb.Booster()
model.load_model('model/churn_model.json')

# ---------------- TITLE ----------------
st.markdown(
    "<h1 style='text-align:center;'>📊 Telecom Customer Churn Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<center>AI-powered churn prediction & retention insights</center>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🧑 Customer Profile")

# Tenure
tenure = st.sidebar.slider(
    "Tenure (Months)",
    0,
    72,
    12
)

# Monthly Charges
monthly_charges_usd = st.sidebar.slider(
    "Monthly Charges (USD)",
    18,
    120,
    70
)

monthly_charges = monthly_charges_usd

st.sidebar.write(
    f"₹ {monthly_charges * 83:.0f}"
)

# Total Charges (Auto Calculate)
total_charges = tenure * monthly_charges

st.sidebar.write(
    f"Estimated Total Charges: ₹ {total_charges * 83:.0f}"
)

# Contract
contract = st.sidebar.selectbox(
    "Contract Type",
    ("Month-to-month", "One year", "Two year")
)

# Internet
internet_service = st.sidebar.selectbox(
    "Internet Service",
    ("Fiber optic", "DSL", "No")
)

# Security
online_security = st.sidebar.selectbox(
    "Online Security",
    ("Yes", "No")
)

# Support
tech_support = st.sidebar.selectbox(
    "Tech Support",
    ("Yes", "No")
)

# Payment
payment_method = st.sidebar.selectbox(
    "Payment Method",
    (
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    )
)

# ---------------- INPUT DATA ----------------
input_data = {
    'tenure': tenure,
    'MonthlyCharges': monthly_charges,
    'TotalCharges': total_charges,
    'gender': 1,
    'SeniorCitizen': 0,
    'Partner': 1,
    'Dependents': 0,
    'PhoneService': 1,
    'PaperlessBilling': 1,
}

# Contract Encoding
input_data['Contract_Month-to-month'] = 1 if contract == "Month-to-month" else 0
input_data['Contract_One year'] = 1 if contract == "One year" else 0
input_data['Contract_Two year'] = 1 if contract == "Two year" else 0

# Internet Encoding
input_data['InternetService_Fiber optic'] = 1 if internet_service == "Fiber optic" else 0
input_data['InternetService_DSL'] = 1 if internet_service == "DSL" else 0
input_data['InternetService_No'] = 1 if internet_service == "No" else 0

# Security Encoding
input_data['OnlineSecurity_Yes'] = 1 if online_security == "Yes" else 0
input_data['OnlineSecurity_No'] = 1 if online_security == "No" else 0

# Support Encoding
input_data['TechSupport_Yes'] = 1 if tech_support == "Yes" else 0
input_data['TechSupport_No'] = 1 if tech_support == "No" else 0

# Payment Encoding
input_data['PaymentMethod_Electronic check'] = 1 if payment_method == "Electronic check" else 0
input_data['PaymentMethod_Mailed check'] = 1 if payment_method == "Mailed check" else 0
input_data['PaymentMethod_Bank transfer (automatic)'] = 1 if payment_method == "Bank transfer (automatic)" else 0
input_data['PaymentMethod_Credit card (automatic)'] = 1 if payment_method == "Credit card (automatic)" else 0

# Fill Missing Features
for col in feature_names:
    if col not in input_data:
        input_data[col] = 0

# ---------------- PREDICTION ----------------
input_df = pd.DataFrame([input_data])[feature_names]

dtest = xgb.DMatrix(input_df)

churn_prob = model.predict(dtest)[0]

# ---------------- KPI METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Tenure",
    f"{tenure} Months"
)

col2.metric(
    "Monthly Charges",
    f"₹ {monthly_charges * 83:.0f}"
)

col3.metric(
    "Churn Risk",
    f"{churn_prob:.2%}"
)

st.markdown("---")

# ---------------- MAIN DASHBOARD ----------------
left_col, right_col = st.columns(2)

# ---------------- LEFT ----------------
with left_col:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Prediction Result")

    st.write(
        f"### {churn_prob:.2%} chance customer will churn"
    )

    st.progress(int(churn_prob * 100))

    if churn_prob > 0.6:
        st.error("⚠️ High Churn Risk")

    elif churn_prob > 0.3:
        st.warning("🟠 Medium Churn Risk")

    else:
        st.success("✅ Low Churn Risk")

    st.markdown('</div>', unsafe_allow_html=True)

    # Customer Summary
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📌 Customer Summary")

    st.write(f"""
    - **Tenure:** {tenure} months
    - **Monthly Charges:** ₹ {monthly_charges * 83:.0f}
    - **Total Charges:** ₹ {total_charges * 83:.0f}
    - **Contract Type:** {contract}
    - **Internet Service:** {internet_service}
    """)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT ----------------
with right_col:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🔍 Key Insights")

    if monthly_charges > 70:
        st.write("👉 High monthly charges increase churn risk")

    if contract == "Month-to-month":
        st.write("👉 Month-to-month contracts have higher churn")

    if tenure < 6:
        st.write("👉 New customers are more likely to churn")

    st.markdown('</div>', unsafe_allow_html=True)

    # Recommended Actions
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("💡 Recommended Actions")

    if churn_prob > 0.6:

        st.write("🔴 High Risk Customer")

        if contract == "Month-to-month":
            st.write("👉 Offer discount for long-term contract")

        if monthly_charges > 70:
            st.write("👉 Provide cheaper plan or bundle offer")

        if tenure < 6:
            st.write("👉 Provide onboarding support")

        st.write("👉 Improve customer support")

    elif churn_prob > 0.3:

        st.write("🟠 Medium Risk Customer")

        st.write("👉 Offer loyalty rewards")
        st.write("👉 Send personalized offers")
        st.write("👉 Improve engagement")

    else:

        st.write("🟢 Low Risk Customer")

        st.write("👉 Upsell premium services")
        st.write("👉 Offer add-ons")

    st.markdown('</div>', unsafe_allow_html=True)
# ---------------- USER REVIEW SECTION ----------------

# Store reviews temporarily
if "reviews" not in st.session_state:
    st.session_state.reviews = []

# Review Card Start
st.markdown('<div class="review-card">', unsafe_allow_html=True)

st.subheader("⭐ Customer Feedback")

st.write("Share your experience with the churn prediction dashboard")

# Review Input
review = st.text_area(
    "Write your review"
)

# Rating Slider
rating = st.slider(
    "Rate this dashboard",
    1,
    5,
    4
)

# Submit Button
if st.button("Submit Review"):

    if review.strip() != "":

        st.session_state.reviews.append({
            "rating": rating,
            "review": review
        })

        st.success("✅ Thank you for your feedback!")

    else:

        st.warning("⚠️ Please enter a review before submitting")

# ---------------- DISPLAY REVIEWS ----------------

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📢 Recent Reviews")

# No Reviews
if len(st.session_state.reviews) == 0:

    st.info("No reviews submitted yet")

# Show Reviews
else:

    for item in st.session_state.reviews[::-1]:

        st.markdown(f"""
        <div class="review-box">

            <div class="review-title">
                ⭐ {item['rating']}/5
            </div>

            <div style="margin-top:8px;">
                📝 {item['review']}
            </div>

        </div>
        """, unsafe_allow_html=True)

# Review Card End
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown("""
<center>

<h4>📊 Telecom Customer Churn Dashboard</h4>

Built using <b>Python, Streamlit, XGBoost & Machine Learning</b>

<br>

© 2026 Customer Analytics System | Designed for Telecom Retention Insights

</center>
""", unsafe_allow_html=True)