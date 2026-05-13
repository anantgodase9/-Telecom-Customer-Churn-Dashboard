# Customer Churn Prediction & Analysis

![Churn Banner](./banner.png)

## Overview

This project analyzes and predicts **customer churn** using a real-world Telco dataset. We explore key factors influencing churn, build predictive models, and create an interactive **Streamlit web app** for churn risk scoring.

**Business Goal**: Identify customers likely to leave and suggest actionable strategies to improve retention.

---

## Key Features

- **End-to-end analysis**: From data cleaning and EDA to model building and business insights.
- **Advanced models**: Logistic Regression, Random Forest, and XGBoost compared and interpreted.
- **Interactive Streamlit app**: Predict churn risk dynamically based on customer features.
- **Business recommendations**: Data-backed insights for churn reduction strategies.

---

## Dataset

- **Telco Customer Churn dataset**: [Download here](https://www.kaggle.com/blastchar/telco-customer-churn)
- Contains customer demographics, services, billing, and churn labels.

---

## Tech Stack

- **Python (pandas, scikit-learn, XGBoost, matplotlib, seaborn)**
- **Streamlit** for web app
- **Jupyter Notebook** for EDA and modeling
- **Git & GitHub Codespaces** for development

---

## Business Insights

- Month-to-month contract customers have **high churn risk** — suggest loyalty programs.  
- Fiber optic customers churn more — consider special retention offers.  
- Customers without security or tech support services are more likely to churn — offer bundled services.
- High monthly charges correlate with churn — provide personalized discount or value packages.

---

## Folder Structure
```
.
├── customer_churn.ipynb # Notebook with EDA and modeling
├── app/
│ ├── streamlit_app.py # Streamlit web app
│ └── model/
│   ├── churn_model.json # Saved XGBoost model
│   └── feature_names.json # Model feature names
├── data/
│ └── WA_Fn-UseC_-Telco-Customer-Churn.csv
├── requirements.txt
├── README.md


```

---

## Streamlit App

**Try it live:** [Streamlit App Link](https://customer-churn-prediction-and-analysis-66prjho2qqhprceqcqnnbo.streamlit.app/)

Or run locally:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Made with love ❤️
