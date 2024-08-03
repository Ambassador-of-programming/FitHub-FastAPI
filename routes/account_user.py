from fastapi import APIRouter, Depends, Form, HTTPException, status, Request, Response
from models.user_model import EditModel, ConnectLessonModel, VerificationLessonModel, VerifiAccountModel
from database.database import LessonsDatabase, AuthDataBase

# Создаем роутер для пользователей
user_router = APIRouter()

# Подтверждение почты
@user_router.post("/user/verifi_email")
async def signin_user(edit: VerifiAccountModel) -> dict:
    db = AuthDataBase()
    await db.confirm_email(edit.email)
    return {
        "message": True
    }

# Получение информации о аккаунте пользователя по его почте
@user_router.post("/user/get_account")
async def signin_user(phone: VerifiAccountModel) -> dict:
    db = AuthDataBase()
    result = await db.get_user_by_email(phone.phone)
    if result:
        return {
            "message": True,
            "user": result
        }
    else:
        return {
            "message": False
        }

# Редактирование аккаунта
@user_router.post("/user/edit_account")
async def signin_user(edit: EditModel) -> dict:
    db = AuthDataBase()
    await db.edit_user(
        edit.phone,
        edit.parametr,
        edit.parametr_value
    )
    return {
        "message": True
    }

# Запись на занятие и подтвердить бронирование
@user_router.post("/user/connect_lesson")
async def signin_user(lesson: ConnectLessonModel) -> dict:
    db = LessonsDatabase()
    await db.user_connect_lesson(
        lesson.user_phone,
        lesson.lesson_id
    )
    return {
        "message": True
    }

# # Подтверждение занятий
# @user_router.post("/user/verify_lesson")
# async def signin_user(lesson: VerificationLessonModel) -> dict:
#     db = AuthDataBase()
#     await db.user_connect_lesson(
#         lesson.user_phone,
#         lesson.trainer_phone
#     )
#     return {
#         "message": True
#     }

# Получение всех занятий
@user_router.get("/user/get_lesson")
async def signin_user() -> dict:
    db = LessonsDatabase()
    return await db.get_lessons()


# Проверка занятия
@user_router.post("/user/check_lesson")
async def signin_user(phone_user: VerifiAccountModel) -> dict:
    db = LessonsDatabase()
    return await db.check_lesson(phone_user=phone_user.phone)