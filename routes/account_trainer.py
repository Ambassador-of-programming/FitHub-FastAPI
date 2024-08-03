from fastapi import APIRouter, Depends, Form, HTTPException, status, Request, Response
from models.trainer_model import AddLessonModel, DeleteLessons, EditModel
from database.database import AuthDataBase, LessonsDatabase

# Создаем роутер для пользователей
trainer_router = APIRouter()

# Добавление занятий
@trainer_router.post("/trainer/add_lessons")
async def signin_user(lesson: AddLessonModel) -> dict:
    db = LessonsDatabase()
    await db.add_lessons(
        lesson.phone_number,
        lesson.lesson_type,
        lesson.lesson_time,
        lesson.lesson_date,
        lesson.lesson_duration,
    )
    
    return {
            "message": True,
        }

# Просмотр занятий по номеру тренара тренера
@trainer_router.post("/trainer/get_lessons")
async def lesson_email_trainer(lesson: DeleteLessons) -> dict:
    db = LessonsDatabase()
    result = await db.get_lesson_id_trainer(lesson.phone_number)
    if result:
        return {
            "message": True,
            "data": result
        }
    else:
        return {
            "message": False,
        }
    

# Просмотр занятий по номеру тренара тренера
@trainer_router.post("/trainer/check_all_lesson_phone")
async def lesson_email_trainer(lesson: DeleteLessons) -> dict:
    db = LessonsDatabase()
    result = await db.get_lesson_phone_trainer(lesson.phone_number)
    if result:
        return {
            "message": True,
            "data": result
        }
    
    else:
        return {
            "message": False,
        }

# Удаление занятий
@trainer_router.post("/trainer/delete_lessons")
async def delete_lessons(lesson: DeleteLessons) -> dict:
    db = LessonsDatabase()
    await db.delete_lessons(
        lesson.email
    )
    
    return {
            "message": True,
        }

# Редактирование аккаунта
@trainer_router.post("/trainer/edit_account")
async def edit_account(edit: EditModel) -> dict:
    db = AuthDataBase()
    await db.edit_user(
        edit.email,
        edit.parametr,
        edit.parametr_value
    )
    
    return {
            "message": True,
        }