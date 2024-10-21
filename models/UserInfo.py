from dataclasses import dataclass


@dataclass
class UserInfo:
    userInfoId: int
    userId: int
    secretInfo: str


