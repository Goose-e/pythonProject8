import re
from servers import IServer


class Masking():
    @staticmethod
    async def maskData(text, maskType,serverInstance: IServer):
        regularsList = await serverInstance.getRegulars()
        if maskType == 1:
            print(maskType)
            text1 = text

            for i in regularsList:
                regulator = re.compile(i.regular_expression)
                text = regulator.sub("***", text)

            def maskRemainingDigits(text):
                text = re.sub(r'\b\d{4,}\b', '***', text)
                text = re.sub(r'\*\*\*\d{2,4}', '***', text)
                return text

            text = maskRemainingDigits(text)

            return text, (text1 == text), text1
        elif maskType == 2:
            print(maskType)
            text1 = text

            for i in regularsList:
                regulator = re.compile(i.regular_expression)
                text = regulator.sub("", text)

            def maskRemainingDigits(text):
                text = re.sub(r'\b\d{4,}\b', '', text)
                text = re.sub(r'\*\*\*\d{2,4}', '', text)
                return text

            text = maskRemainingDigits(text)
            return text, (text1 == text), text1
        elif maskType == 3:
            try:
                print(maskType)

                for i in regularsList:
                    regulator = re.compile(i.regular_expression)
                    text = regulator.sub("***", text)

                def maskRemainingDigits(text):
                    text = re.sub(r'\b\d{4,}\b', '***', text)
                    text = re.sub(r'\*\*\*\d{2,4}', '***', text)
                    return text
                text1 = text
                text = maskRemainingDigits(text)
                return text, (text1 == text), text1
            except:
                return
