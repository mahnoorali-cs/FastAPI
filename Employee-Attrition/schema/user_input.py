from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated

#pydantic model for input data validation
class UserInput(BaseModel):
    Age: Annotated[int, Field(..., ge=18, le=100, description="Age of the employee")]
    Gender: Annotated[Literal["Male", "Female"], Field(..., description="Gender of the employee")]
    DailyRate: Annotated[int, Field(..., ge=0, description="Daily rate of the employee")]
    HourlyRate: Annotated[int, Field(..., ge=0, description="Hourly rate of the employee")]
    DistanceFromHome: Annotated[int, Field(..., ge=0, description="Distance from home in miles")]
    Education: Annotated[int, Field(..., ge=1, le=5, description="Education level (1-5)")]
    EducationField: Annotated[Literal["Human Resources", "Life Sciences", "Marketing", "Medical", "Other", "Technical Degree"], Field(..., description="Field of education")]
    EnvironmentSatisfaction: Annotated[int, Field(..., ge=1, le=5, description="Environment satisfaction level (1-5)")]
    JobLevel: Annotated[int, Field(..., ge=1, le=5, description="Job level (1-5)")]
    JobRole: Annotated[
        Literal[
            "Healthcare Representative", "Human Resources", "Laboratory Technician", "Manager",
            "Manufacturing Director", "Research Director", "Research Scientist",
            "Sales Executive", "Sales Representative"],Field(..., description="Job role of the employee")
    ]
    JobSatisfaction: Annotated[int, Field(..., ge=1, le=5, description="Job satisfaction level (1-5)")]
    MonthlyIncome: Annotated[int, Field(..., ge=0, description="Monthly income of the employee")]
    NumCompaniesWorked: Annotated[int, Field(..., ge=0, description="Number of companies worked for")]
    PerformanceRating: Annotated[int, Field(..., ge=1, le=5, description="Performance rating (1-5)")]
    MaritalStatus: Annotated[Literal["Single", "Married", "Divorced"], Field(..., description="Marital status of the employee")]
    OverTime: Annotated[Literal["Yes", "No"], Field(..., description="Whether the employee works overtime")]
    BusinessTravel: Annotated[Literal["Non-Travel", "Travel_Rarely", "Travel_Frequently"], Field(..., description="Business travel frequency")]
    Department: Annotated[Literal["Sales", "Research & Development", "Human Resources"], Field(..., description="Department of the employee")]
    TotalWorkingYears: Annotated[int, Field(..., ge=0, description="Total working years of the employee")]
    WorkLifeBalance: Annotated[int, Field(..., ge=1, le=5, description="Work-life balance level (1-5)")]
    YearsAtCompany: Annotated[int, Field(..., ge=0, description="Years at the company")]
    YearsInCurrentRole: Annotated[int, Field(..., ge=0, description="Years in the current role")]
    YearsSinceLastPromotion: Annotated[int, Field(..., ge=0, description="Years since the last promotion")]
    YearsWithCurrManager: Annotated[int, Field(..., ge=0, description="Years with the current manager")]

    @field_validator('JobRole', 'MaritalStatus', 'OverTime', 'BusinessTravel', 'Department')
    @classmethod
    def validate_categorical_fields(cls, v:str) -> str:
        v=v.strip().title()
        return v

    @computed_field
    @property
    def IncomePerYearExp(self) -> float:
        return self.MonthlyIncome / (self.TotalWorkingYears + 1)

    @computed_field
    @property
    def YearsAtCompanyRatio(self) -> float:
        return self.YearsAtCompany / (self.TotalWorkingYears + 1)

    @computed_field
    @property
    def PromotionGap(self) -> int:
        return self.YearsAtCompany - self.YearsSinceLastPromotion

    @computed_field
    @property
    def AvgSatisfaction(self) -> float:
        return (self.EnvironmentSatisfaction + self.JobSatisfaction + self.WorkLifeBalance) / 3
