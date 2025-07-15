from pydantic import BaseModel, EmailStr, constr

class PatientBase(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    phone: constr(min_length=7, max_length=20)

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    id: int
    document_photo: str

    class Config:
        orm_mode = True 