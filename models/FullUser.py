from dataclasses import dataclass
from datetime import  date

@dataclass
class FullUser:
    user_id: int
    email: str

    login: str
    support_level: int
    age: int
    birthdate: date
    first_name: str
    phone_number: str
    middle_name: str
    gender: str
    last_name: str
