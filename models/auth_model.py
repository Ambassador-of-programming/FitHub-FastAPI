from pydantic import BaseModel, validator, EmailStr
from fastapi import HTTPException, status

class LoginModel(BaseModel):
    phone_number: str
    password: str
    
    @validator('password')
    def password_length(cls, password):
        if len(password) >= 8 and len(password) <= 40:
            return password
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="The length of the password must be from 8 and up to 40"
            )

class SignupModel(BaseModel):
    phone_number: str
    password: str
    fio: str
    type_user: str
    
    @validator('password')
    def password_length(cls, password):
        if len(password) >= 7 and len(password) <= 40:
            return password
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="The length of the password must be from 8 and up to 40"
            )