from fastapi import FastAPI, Path, HTTPException, Query 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional 
import json 

app = FastAPI()

class Patient(BaseModel):

    id:Annotated[str, Field(..., description="The ID of the patient", example='P001')]
    name:Annotated[str, Field(..., description="The name of the patient")]
    city:Annotated[str, Field(..., description="The city where patient is living")]
    age:Annotated[int, Field(..., description="The age of the patient", ge=0, le=120)]
    gender:Annotated[Literal['male', 'female', 'other'], Field(..., description='The gender of the patient')]
    height:Annotated[float, Field(..., description="The height of the patient in meters", ge=0)]
    weight:Annotated[float, Field(..., description="The weight of the patient in kilograms", ge=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name:Annotated[Optional[str], Field(default=None)]
    city:Annotated[Optional[str], Field(default=None)]
    age:Annotated[Optional[int], Field(default=None, ge=0)]
    gender:Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]
    height:Annotated[Optional[float], Field(default=None, ge=0)]
    weight:Annotated[Optional[float], Field(default=None, ge=0)]


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get("/") 
def hello(): 
    return {"message": "Patient Management System API"}  

#run it with the help of uvicorn server

@app.get("/about")
def about():
    return {"message": "A fully functinal API to manage patients and their medical records."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description='Sort on the bais of height, weight or bmi'), order: str = Query('asc', description='Sort in asc or desc order')):

    valid_feilds = ['height', 'weight', 'bmi']
    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Must be one of {valid_feilds}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #check if patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail=f"Patient with ID {patient.id} already exists.")

    #add new patient to data
    data[patient.id] = patient.model_dump(exclude=['id'])    #convert pydantic object to dict

    #save uinto the json file
    save_data(data)

    return JSONResponse(status_code=201, content={"message": f"Patient with ID {patient.id} created successfully."})

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)  # Get only the fields that were provided in the update request

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id  # add id feild as pydantic model requires it to be present but it is not in update model 
    patient_pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude={'id'})  # Convert the updated Pydantic object to a dictionary, excluding the 'id' field

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={"message": f"Patient with ID {patient_id} updated successfully."})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": f"Patient with ID {patient_id} deleted successfully."})
