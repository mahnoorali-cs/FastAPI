from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION
from schema.user_input import UserInput

app = FastAPI()

#human readable endpoint, that api is running
@app.get("/")
def home():
    return {"message": "Welcome to the Employee Attrition Prediction API."}

#machine readable, cloud service health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_version": MODEL_VERSION,
        "model_loaded" : model is not None
    }


@app.post("/predict", response_model= PredictionResponse, status_code=200)
def predict_attrition(data: UserInput):

    user_input = pd.DataFrame([{
        "Age": data.Age,
        "Gender": data.Gender,
        "DailyRate": data.DailyRate,
        "HourlyRate": data.HourlyRate,
        "DistanceFromHome": data.DistanceFromHome,
        "Education": data.Education,
        "EducationField": data.EducationField,
        "EnvironmentSatisfaction": data.EnvironmentSatisfaction,
        "JobLevel": data.JobLevel,
        "JobRole": data.JobRole,
        "JobSatisfaction": data.JobSatisfaction,
        "MonthlyIncome": data.MonthlyIncome,
        "NumCompaniesWorked": data.NumCompaniesWorked,
        "PerformanceRating": data.PerformanceRating,
        "MaritalStatus": data.MaritalStatus,
        "OverTime": data.OverTime,
        "BusinessTravel": data.BusinessTravel,
        "Department": data.Department,
        "TotalWorkingYears": data.TotalWorkingYears,
        "WorkLifeBalance": data.WorkLifeBalance,
        "YearsAtCompany": data.YearsAtCompany,
        "YearsInCurrentRole": data.YearsInCurrentRole,
        "YearsSinceLastPromotion": data.YearsSinceLastPromotion,
        "YearsWithCurrManager": data.YearsWithCurrManager,
        "IncomePerYearExp": data.IncomePerYearExp,
        "YearsAtCompanyRatio": data.YearsAtCompanyRatio,
        "PromotionGap": data.PromotionGap,
        "AvgSatisfaction": data.AvgSatisfaction
    }])

    try:
        result = predict_output(user_input)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))


