from pydantic import BaseModel, EmailStr

class EditModel(BaseModel):
    phone: str
    parametr: str
    parametr_value: str

class ConnectLessonModel(BaseModel):
    user_phone: str
    lesson_id: str

class VerificationLessonModel(BaseModel):
    user_phone: str
    trainer_phone: str

class VerifiAccountModel(BaseModel):
    phone: str
    