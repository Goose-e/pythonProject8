#Класс в данном виде не работает
#Это просто обязательные методы для модуля flask_login


class UserLogin():
    def fromBD(self, userID, DB):
        self.__user=DB.getUserID(userID)
        return  self

    def get_user(self):
        return self.__user

    def createUser(self, user):
        self.__user=user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonnymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])