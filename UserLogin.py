from quart_auth import AuthUser

from servers.reverseServer1 import authAdmin


def createUser(user) -> 'UserLogin':
    return UserLogin(id = user.adminId, login =user.adminLogin, password =user.adminPassword)

class UserLogin(AuthUser):
    def __init__(self, id, login, password):  # Добавляем параметр auth_id
        super().__init__(2)  # Вызов конструктора родительского класса
        self.userId = id
        self.userLogin = login
        self.userPassword = password


    def get_user(self):
        return self

    def is_authenticated(self):
        return self.is_active()

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.userId) if self.userId is not None else str(None)
