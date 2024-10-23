from dataclasses import dataclass
from datetime import  datetime

@dataclass
class UserInfo:
    userInfoId: int
    userId: int
    secretInfo: str
    endpoint: str
    timestamp: str


