from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
import json

app=FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Enter ID of Patient",examples=['P001', 'P002'])]
    name: Annotated[str, Field(..., description="Enter name of Patient",examples=['John'])]
    city: Annotated[str, Field(..., description="Enter city of Patient",examples=['Mumbai', 'Delhi'])]
    age: Annotated[int, Field(..., description="Enter age of Patient",examples=[25, 30])]
    gender: Annotated[str, Field(..., description="Enter gender of Patient",examples=['Male', 'Female'])]
    height: Annotated[float, Field(..., gt=0,description="Enter height of Patient")]
    weight: Annotated[float, Field(...,gt=0, description="Enter weight of Patient")]

#Pydantic for Update class
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(description="Enter name of Patient",examples=['John'])]
    city: Annotated[Optional[str], Field(description="Enter city of Patient",examples=['Mumbai', 'Delhi'])]
    age: Annotated[Optional[int], Field(description="Enter age of Patient",examples=[25, 30])]
    gender: Annotated[Optional[str], Field(description="Enter gender of Patient",examples=['Male', 'Female'])]
    height: Annotated[Optional[float], Field(gt=0,description="Enter height of Patient")]
    weight: Annotated[Optional[float], Field(gt=0, description="Enter weight of Patient")]

    @computed_field
    @property
    def bmi(self) -> int:
       bmi= round(self.weight/(self.height**2))
       return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return "Underweight"
        elif self.bmi < 24.9:
            return "Normal"
        elif self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

def load_data():
    with open('patients.json','r')as f:
        data=json.load(f)
    return data

def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data,f)
@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get("/patient")
def get_patient():
    return {'message': 'Get all patient records'}
@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    # load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exist")
    data[patient.id]=patient.model_dump(exclude=["id"])

    save_data(data)
    return JSONResponse(status_code=201, content={"mesage":"Patient Addded Successfully"})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, pateint_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    
    existing_patient_info= data[patient_id]
    update_patient_info=pateint_update.model_dump(exclude_unset=True)

    for key,value in update_patient_info.items():
        existing_patient_info[key]=value

    existing_patient_info['id']=patient_id
    patient_pydantic_object=Patient(**existing_patient_info)
    existing_patient_info=patient_pydantic_object.model_dump(exclude="id")

    data[patient_id]= patient_pydantic_object
    save_data(data)

    return JSONResponse(status=200, content={"message": "Patient updated successfully"})