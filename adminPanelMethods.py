from consts import masking_instance


class adminControl():

    @staticmethod
    async def changeMaskMethod(maskMethodType):
        masking_instance.set_mask_type(maskMethodType)

    # @staticmethod
    # async def addRegularExpression(Expression):
    #     await asyncio.to_thread(DaBa().saveInfoInRegular, Expression)
    #
    # @staticmethod
    # async def addReaderSource(sourceAdress):
    #     pass
    #     await asyncio.to_thread(DaBa().saveSource, sourceAdress)
