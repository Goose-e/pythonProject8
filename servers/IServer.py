from abc import ABC, abstractmethod


class IServer(ABC):
    @abstractmethod
    async def getRegulars(self):
        regulars = await self.getRegulars()
        pass
