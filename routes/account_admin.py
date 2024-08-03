from fastapi import APIRouter, Depends, Form, HTTPException, status, Request, Response
from models.admin_model import DeleteLessons, DeleteModel, EditLessonsModel
from models.user_model import EditModel
from database.database import AuthDataBase, LessonsDatabase

# Создаем роутер для пользователей
admin_router = APIRouter()

# Получить всех пользователей
@admin_router.get('/admin/get_all_users')
async def get_all_users():
    db = AuthDataBase()
    return {
        "message": True,
        "data": await db.get_all_users()
    }

# Получение всех пользователей с типом "user"
@admin_router.get('/admin/get_all_type_user')
async def get_all_users_user():
    db = AuthDataBase()
    return {
        "message": True,
        "data": await db.get_all_type_users()
    }

# Получение всех пользователей с типом "trainer"
@admin_router.get('/admin/get_all_type_trainer')
async def get_all_users_trainer():
    db = AuthDataBase()
    return {
        "message": True,
        "data": await db.get_all_type_trainer()
    }

# Получить все занятия и тренеров
@admin_router.get('/admin/get_all_lessons')
async def get_all_lessons():
    db = LessonsDatabase()
    return {
        "message": True,
        "data": await db.get_all_lesson()
    }

# Удаления пользователя по почте
@admin_router.post("/admin/delete_user")
async def signin_user(email: DeleteModel) -> dict:
    db = AuthDataBase()
    await db.delete_user(
        email.email
    )
    return {
        "message": True,
    }

# Удаление занятий по email тренера
@admin_router.post("/admin/delete_lesson")
async def signin_user(email: DeleteLessons) -> dict:
    db = LessonsDatabase()
    await db.delete_lessons(
        email.email
    )

# Редактирование занятий по емайл тренера
@admin_router.post('/admin/edit_lesson')
async def edit_lesson(edit: EditLessonsModel):
    db = LessonsDatabase()
    await db.edit_lesson(
        edit.email,
        edit.parametr,
        edit.parametr_value
    )


# Редактирование аккаунта
@admin_router.post("/admin/edit")
async def signin_user(edit: EditModel) -> dict:
    db = AuthDataBase()
    await db.edit_user(
        edit.email,
        edit.parametr,
        edit.parametr_value
    )

