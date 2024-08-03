from fastapi import APIRouter, Depends, Form, HTTPException, status, Request, Response
from models.auth_model import LoginModel, SignupModel
from database.database import AuthDataBase

# Создаем роутер для пользователей
auth_router = APIRouter()

# POST запрос на авторизацию
@auth_router.post("/signin")
async def signin_user(login: LoginModel) -> dict:
    db = AuthDataBase()
    result = await db.auth_user(
        phone_number=login.phone_number, password=login.password)
    
    if result['status'] == True:
        return {
            "message": True,
            "user_type": result['user_type']
        }
    
    else:
        return {
            "message": False
        }

# POST запрос на регистрацию
@auth_router.post("/signup")
async def signup_user(signup: SignupModel):
    db = AuthDataBase()

    # Проверяем, есть ли результаты запроса
    result = await db.singup_user(
        phone_number=signup.phone_number, password=signup.password, fio=signup.fio,
        type_user=signup.type_user)
    
    if result == True:
        return {
            "message": True
        }
    
    else:
        return {
            "message": False
        }