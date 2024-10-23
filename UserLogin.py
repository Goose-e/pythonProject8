class UserLogin:
    async def fromBD(self, userID, DB):
        self.__user = await DB.getUserByID(userID)
        self.is_authenticated = True
        return self

    def get_user(self):
        return self.__user

    async def createUser(self, user):
        self.__user = user
        return self

    async def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.adminId)
