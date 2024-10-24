from dataclasses import dataclass


@dataclass
class ModelForLogin:
    adminId: int
    adminLogin: str
    adminPassword: str

    def get_id(self):
        return str(self.adminId)
    def is_authenticated(self):
        return True