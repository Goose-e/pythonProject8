from maskMethods import Masking
from db import DaBa
import asyncio


class adminControl():
    @staticmethod
    async def changeMaskMethod(maskMethodType):
        await Masking.changeMaskType(maskMethodType)

    @staticmethod
    async def addRegularExpression(Expression):
        await asyncio.to_thread(DaBa().saveInfoInRegular, Expression)

    @staticmethod
    async def addReaderSource(sourceAdress):
        pass
        await asyncio.to_thread(DaBa().saveSource, sourceAdress)
