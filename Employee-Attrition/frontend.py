import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Employee Attrition Prediction")

st.markdown("Enter the employee details below to predict whether they are likely to leave the company.")

#input fields for the user to enter employee details
Age = st.number_input("Age", min_value=18, max_value=65, value=30)
Gender = st.selectbox("Gender", ["Male", "Female"])
DailyRate = st.number_input("Daily Rate", min_value=0, value=100)
HourlyRate = st.number_input("Hourly Rate", min_value=0, value=60)
DistanceFromHome = st.number_input("Distance From Home (in miles)", min_value=0, value=10)
Education = st.selectbox("Education Level", [1, 2, 3, 4, 5])
EducationField = st.selectbox(
    "Education Field",
    ["Human Resources", "Life Sciences", "Marketing", "Medical", "Other", "Technical Degree"]
)
EnvironmentSatisfaction = st.selectbox("Environment Satisfaction Level", [1, 2, 3, 4, 5])
JobLevel = st.selectbox("Job Level", [1, 2, 3, 4, 5])
JobRole = st.selectbox(
    "Job Role",
    [
        "Healthcare Representative", "Human Resources", "Laboratory Technician", "Manager",
        "Manufacturing Director", "Research Director", "Research Scientist",
        "Sales Executive", "Sales Representative"
    ]
)
JobSatisfaction = st.selectbox("Job Satisfaction Level", [1, 2, 3, 4, 5])
MonthlyIncome = st.number_input("Monthly Income", min_value=0, value=5000)
NumCompaniesWorked = st.number_input("Number of Companies Worked For", min_value=0, value=1)
PerformanceRating = st.selectbox("Performance Rating", [1, 2, 3, 4, 5])
MaritalStatus = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
OverTime = st.selectbox("Overtime", ["Yes", "No"])
BusinessTravel = st.selectbox("Business Travel Frequency", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
Department = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
TotalWorkingYears = st.number_input("Total Working Years", min_value=0, value=5)
WorkLifeBalance = st.selectbox("Work-Life Balance Level", [1, 2, 3, 4, 5])
YearsAtCompany = st.number_input("Years at the Company", min_value=0, value=3)
YearsInCurrentRole = st.number_input("Years in Current Role", min_value=0, value=2)
YearsSinceLastPromotion = st.number_input("Years Since Last Promotion", min_value=0, value=1)
YearsWithCurrManager = st.number_input("Years with Current Manager", min_value=0, value=2)

if st.button("Predict Attrition"):

    # --- Derived/engineered fields required by the backend schema ---
    # These four are not raw user inputs; they're computed from the fields above,
    # the same way they must have been computed when the model was trained.
    IncomePerYearExp = MonthlyIncome / TotalWorkingYears if TotalWorkingYears > 0 else 0
    YearsAtCompanyRatio = YearsAtCompany / TotalWorkingYears if TotalWorkingYears > 0 else 0
    PromotionGap = YearsAtCompany - YearsSinceLastPromotion
    AvgSatisfaction = (EnvironmentSatisfaction + JobSatisfaction + WorkLifeBalance) / 3

    input_data = {
        "Age": Age,
        "Gender": Gender,
        "DailyRate": DailyRate,
        "HourlyRate": HourlyRate,
        "DistanceFromHome": DistanceFromHome,
        "Education": Education,
        "EducationField": EducationField,
        "EnvironmentSatisfaction": EnvironmentSatisfaction,
        "JobLevel": JobLevel,
        "JobRole": JobRole,
        "JobSatisfaction": JobSatisfaction,
        "MonthlyIncome": MonthlyIncome,
        "NumCompaniesWorked": NumCompaniesWorked,
        "PerformanceRating": PerformanceRating,
        "MaritalStatus": MaritalStatus,
        "OverTime": OverTime,
        "BusinessTravel": BusinessTravel,
        "Department": Department,
        "TotalWorkingYears": TotalWorkingYears,
        "WorkLifeBalance": WorkLifeBalance,
        "YearsAtCompany": YearsAtCompany,
        "YearsInCurrentRole": YearsInCurrentRole,
        "YearsSinceLastPromotion": YearsSinceLastPromotion,
        "YearsWithCurrManager": YearsWithCurrManager,
        "IncomePerYearExp": IncomePerYearExp,
        "YearsAtCompanyRatio": YearsAtCompanyRatio,
        "PromotionGap": PromotionGap,
        "AvgSatisfaction": AvgSatisfaction
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            predicted_category = result["predicted_category"]
            confidence = result["confidence"]
            class_probabilities = result["class_probabilities"]

            label = "Likely to Leave" if predicted_category == 1 else "Not Likely to Leave"
            st.success(f"Prediction: {label}  (confidence: {confidence:.2%})")

            st.subheader("Class Probabilities")
            st.bar_chart(class_probabilities)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Please ensure the backend server is running.")
