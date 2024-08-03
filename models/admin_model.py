from pydantic import BaseModel, EmailStr

class DeleteModel(BaseModel):
    email: EmailStr

class DeleteLessons(BaseModel):
    email: EmailStr

class EditLessonsModel(BaseModel):
    email: EmailStr
    parametr: str
    parametr_value: str