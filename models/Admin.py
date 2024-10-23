from dataclasses import dataclass


@dataclass
class Admin:
    adminId: int
    adminLogin: str
    adminPassword: str

    def get_id(self):
        return str(self.adminId)
