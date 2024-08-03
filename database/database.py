import aiosqlite
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_name = 'database/db_file.db'

    # подключение к базе данных
    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_name)

    # закрытие подключения к базе данных
    async def close(self):
        if self.connection:
            await self.connection.close()
    
    # выполнение запроса
    async def execute_query(self, query, *args):
        async with self.connection.execute(query, args) as cursor:
            return await cursor.fetchall()
     
    # выполнение записи в базу данных
    async def execute_write_query(self, query, *args):
        async with self.connection.execute(query, args) as cursor:
            await self.connection.commit()

class AuthDataBase(DatabaseManager):
    def __init__(self):
        super().__init__()
    
    async def create_db(self):
        await self.connect()
        await self.execute_write_query('''CREATE TABLE IF NOT EXISTS auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fio TEXT NOT NULL,
            type_user TEXT NOT NULL,
            date_reg TEXT NOT NULL
        )''')
        await self.close()

    # удаление базы данных
    async def drop_db(self):
        await self.connect()
        await self.execute_write_query('''DROP TABLE IF EXISTS auth''')
        await self.close()

    # Получение всех пользователей
    async def get_all_users(self):
        await self.connect()
        query = '''SELECT * FROM auth '''
        result = await self.execute_query(query)
        await self.close()
        return result

    # Получение всех пользователей с типом "user"
    async def get_all_type_users(self):
        await self.connect()
        query = '''SELECT * FROM auth WHERE type_user = 'user' '''
        result = await self.execute_query(query)
        await self.close()
        return result
    
    # Получение всех пользователей с типом "trainer"
    async def get_all_type_trainer(self):
        await self.connect()
        query = '''SELECT * FROM auth WHERE type_user = 'trainer' '''
        result = await self.execute_query(query)
        await self.close()
        return result

    # Получение информации о пользователе по его phone_number
    async def get_user_by_email(self, phone_number):
        await self.connect()
        query = '''SELECT * FROM auth WHERE phone_number =?'''
        result = await self.execute_query(query, phone_number)
        await self.close()
        return result
    
    # Проверка есть ли пользователь в базе данныз
    async def check_user(self, phone_number):
        await self.connect()
        query = '''SELECT * FROM auth WHERE phone_number =?'''
        result = await self.execute_query(query, phone_number)
        await self.close()

        # Проверяем, есть ли результаты запроса
        if result:
            # Если результаты есть, значит, пользователь существует с заданным phone_number
            return True
        else:
            # Если результаты пусты, значит, такого пользователя нет
            return False
        
    # Проверка типа пользователя
    async def check_type_user(self, phone_number: str):
        await self.connect()
        query = '''SELECT type_user FROM auth WHERE phone_number = ?'''
        result = await self.execute_query(query, phone_number)
        await self.close()
        if result:
            return result[0][0]
        else:
            return False


    # Авторизация по почте и паролю
    async def auth_user(self, phone_number, password):
        '''
        Проверка что пользователь по его
        email и password существует в базе данных. 
        Если пользователь есть в базе данных то вернет True иначе False
        '''
        await self.connect()
        query = '''SELECT * FROM auth WHERE phone_number = ? AND password = ?'''
        result = await self.execute_query(query, phone_number, password)
        await self.close()

        # Проверяем, есть ли результаты запроса
        if result:
            user_types = await self.check_type_user(phone_number)
            if user_types:
                # Если результаты есть, значит, пользователь существует с заданным email и password
                return {"status": True,
                        "user_type": user_types}
            
            return {"status": False}
        else:
            # Если результаты пусты, значит, такого пользователя нет
            return {"status": False}
    
    # Регистрация пользователя
    async def singup_user(self, phone_number, password, fio, type_user):
        '''
        Создание нового пользователя в базе данных
        '''
        check_email = await self.check_user(phone_number)

        if check_email == True:
            return False
        
        await self.connect()
        query = '''INSERT INTO auth (phone_number, password, fio, type_user, date_reg) VALUES (?,?,?,?,?)'''
        await self.execute_write_query(query, phone_number, password, fio, type_user, datetime.now())
        await self.close()

        return True
    
    # Редактирование аккаунта
    async def edit_user(self, phone_number: str, parametr: str, parametr_value: str):
        await self.connect()
        query = f'UPDATE auth SET {parametr} = "{parametr_value}" WHERE phone_number = "{phone_number}"'
        await self.execute_write_query(query, )
        await self.close()

    # Удаление пользователя
    async def delete_user(self, phone_number: str):
        await self.connect()
        query = f'DELETE FROM auth WHERE phone_number = "{phone_number}"'
        await self.execute_write_query(query, )
        await self.close()

    async def drop(self):
        await self.connect()
        query = '''DROP TABLE IF EXISTS auth'''
        await self.execute_write_query(query)
        await self.close()
            
class LessonsDatabase(DatabaseManager):
    def __init__(self):
        super().__init__()
    
    async def create_db(self):
        await self.connect()
        await self.execute_write_query('''CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL,
            lesson_type TEXT,
            lesson_time TEXT,
            lesson_date TEXT,
            lesson_duration TEXT,
            people_enrolled TEXT
        )''')
        await self.close()

    # Подсчитать всех занятий в базе данных
    async def get_all_lesson(self):
        await self.connect()
        query = '''SELECT * FROM lessons'''
        result = await self.execute_query(query)
        await self.close()
        return len(result)
    
    # добавить занятие
    async def add_lessons(self, phone_number, lesson_type, lesson_time, lesson_duration, lesson_date):
        await self.connect()
        query = '''INSERT INTO lessons (phone_number, lesson_type, lesson_time, lesson_duration, lesson_date) VALUES (?,?,?,?,?)'''
        await self.execute_write_query(query, phone_number, lesson_type, lesson_time, lesson_duration, lesson_date)
        await self.close()

    # удалить занятие
    async def delete_lessons(self, phone_number):
        await self.connect()
        query = '''DELETE FROM lessons WHERE phone_number =?'''
        await self.execute_write_query(query, phone_number)
        await self.close()

    # получить данные о занятиях по номеру тренера
    async def get_lesson_id_trainer(self, id: str):
        await self.connect()
        query = '''SELECT * FROM lessons WHERE id =?'''
        result = await self.execute_query(query, id)
        await self.close()
        return result

    # получить данные о занятиях по номеру тренера
    async def get_lesson_phone_trainer(self, phone_number: str):
        await self.connect()
        query = '''SELECT * FROM lessons WHERE phone_number =?'''
        result = await self.execute_query(query, phone_number)
        await self.close()
        return result
    
    # получить все занятия
    async def get_lessons(self):
        await self.connect()
        query = '''SELECT * FROM lessons'''
        result = await self.execute_query(query)
        await self.close()
        try:
            return {
                'message': True,
                'data': result
            }
        except:
            return {
                'message': False
            }
        
    # получить все занятия пользователя по номеру телефона
    async def check_lesson(self, phone_user: str):
        await self.connect()

        query = f"SELECT * FROM lessons WHERE people_enrolled LIKE '{phone_user}'"
        result = await self.execute_query(query)

        await self.close()

        try:
            return {'message': True, 'data': result}
        except:
            return {'message': False}
    
    # редактировать занятия
    async def edit_lessons(self, phone_number, parametr, parametr_value):
        await self.connect()
        query = f'UPDATE lessons SET "{parametr}" ="{parametr_value}" WHERE phone_number ="{phone_number}"'
        await self.execute_write_query(query)
        await self.close()

    # Записаться на занятия и подтвердить бронирование
    async def user_connect_lesson(self, phone_user: str, id_lesson: str):
        try:
            await self.connect()
    
            # Обновляем запись в базе данных
            query_update = f'''UPDATE lessons SET people_enrolled = "{phone_user}" WHERE id = "{id_lesson}"'''
            await self.execute_write_query(query_update)
            return True
        
        except Exception as e:
            print(f"An error occurred while connecting user to lesson: {e}")
            return False
        finally:
            await self.close()
    
    # удаление базы даннных
    async def drop_db(self):
        await self.connect()
        query = '''DROP TABLE IF EXISTS lessons'''
        await self.execute_write_query(query)
        await self.close()
    
import asyncio

async def main():
    get = AuthDataBase()
    await get.create_db()
    # await get.user_connect_lesson(
    #     '0', '1'
    # )
    # result = await get.add_lessons(
    #     phone_number='trainer',
    #     lesson_type='тип занятия',
    #     lesson_time='время занятия',
    #     lesson_duration='описание',
    #     lesson_date='дата занятия'
    # )
    # result =await get.check_lesson('0')
    # print(result)
if __name__ == '__main__':
    asyncio.run(main())