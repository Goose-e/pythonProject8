from dataclasses import dataclass


@dataclass
class Admin:
    userInfoId: int
    userId: int
    secretInfo: str
