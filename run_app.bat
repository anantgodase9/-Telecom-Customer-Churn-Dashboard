@echo off
cd /d D:\churn_app\app
call venv\Scripts\activate
python -m streamlit run streamlit_app.py
pause