import asyncio
from flask_login import UserMixin


async def fromBD(userID: int, DB):
    """Асинхронное получение пользователя из базы данных"""
    __user = await DB.getUserByID(userID)
    return __user

class UserLogin(UserMixin):
    def __init__(self):
        self.__user = None

    def get_user(self):
        """Возвращает текущего пользователя"""
        return self.__user

    async def createUser(self, user) -> 'UserLogin':
        """Создание нового пользователя"""
        self.__user = user
        return self



    async def is_authenticated(self) -> bool:
        """Проверка, аутентифицирован ли пользователь"""
        return self.__user is not None

    def is_active(self) -> bool:
        """Проверка, активен ли пользователь"""
        return True

    def is_anonymous(self) -> bool:
        """Проверка, является ли пользователь анонимным"""
        return self.__user is None

    def get_id(self) -> str:
        """Получение идентификатора пользователя"""
        if self.__user is not None:
            return str(self.__user.adminId)
        return None
