from dataclasses import dataclass
from datetime import date


@dataclass
class FullUser:
    user_id: int
    email: str
    login: str
    support_level: str
    age: int = None
    birthdate: date = None
    first_name: str = None
    phone_number: str = None
    second_name: str = None
    gender: str = None
    last_name: str = None
