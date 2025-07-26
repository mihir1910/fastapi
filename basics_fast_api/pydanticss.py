from pydantic import BaseModel,EmailStr, AnyUrl, Field
from typing import List,Dict,Optional, Annotated

class Patient(BaseModel):
    name: str=Field(max_length=100)
    age: int=Field(gt=0,lt=120)
    email: EmailStr
    linkedinurl: Optional[AnyUrl]=None
    weight: int=Field(gt=0)
    married: Optional[bool]=False
    allergies: List[str]
    contact_details: Dict[str,str]

def inser_patient(patient:Patient):
    print(patient.name)
    #print(patient.email)
    print(patient.age)
    print(patient.married)
    print("Inserted")

def update_patient(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("Updated")

patient_info={"name":"Raj", "age":24,"email":"abc@example.con","weight":70,"allergies":['diabities','pressure'],"contact_details":{"phone":"9876543210"}}

patient1=Patient(**patient_info)
inser_patient(patient1)
update_patient(patient1)