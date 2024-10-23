class UserLogin:
    def fromBD(self, userID, DB):
        self.__user = DB.getUserByID(userID)
        return self

    def get_user(self):
        return self.__user

    def createUser(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.adminId)