from pydantic import BaseModel, EmailStr

class AddLessonModel(BaseModel):
    phone_number: str
    lesson_type: str
    lesson_time: str
    lesson_date: str
    lesson_duration: str

class DeleteLessons(BaseModel):
    phone_number: str

class EditModel(BaseModel):
    phone_number: str
    parametr: str
    parametr_value: str
