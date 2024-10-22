import re
import asyncio
from enumMask import Mask


class SingletonMeta(type):
    """Метакласс для реализации одиночки."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Masking(metaclass=SingletonMeta):
    def __init__(self):
        self.num = 0

    def set_mask_type(self, mask_type):
        if isinstance(mask_type, Mask):
            self.mask_type = mask_type
            print(f"Mask type set to: {self.mask_type.name}")
        else:
            raise ValueError("Invalid mask type")

    def mask_data(self, text):
        patterns = {
            "phone": re.compile(
                r"(?<!\w)(\+?\d{1,3}[-\s]?)?(\(?\d{2,4}\)?[-\s]?)(\d{1,3}[-\s]?)(\d{1,2}[-\s]?)(\d{2,3})(?!\w)",
                re.VERBOSE),
            "passport": re.compile(r"\b\d{4}[-\s]?\d{6}\b|\b[A-Z]{2}\d{7}\b", re.VERBOSE),
            "card": re.compile(r"(?<!\w)(?:\d{4}[-\s]?){3}\d{4}\b|\d{16}\b", re.VERBOSE),
            "account": re.compile(r"(?<!\w)(?:\d{4}[-\s]?){4}\d{4}\b", re.VERBOSE),
            "date": re.compile(
                r"(\b\d{2}[-./]\d{2}[-./]\d{4}\b)|(\b\d{4}[-./]\d{2}[-./]\d{2}\b)|(\b\d{2}\s\w{3,}\s\d{4}\b)",
                re.VERBOSE),
            "name": re.compile(
                r"(?<!\w)(\b[A-ZА-ЯЁ][a-zа-яё]+\s[A-ZА-ЯЁ][a-zа-яё]+\b)|(\b[A-ZА-ЯЁ]\.\s[A-ZА-ЯЁ][a-zа-яё]+\b)|(\b[A-ZА-ЯЁ]\.\s[A-ZА-ЯЁ]\.\s[A-ZА-ЯЁ][a-zа-яё]+\b)",
                re.VERBOSE),
            "address": re.compile(
                r"(?<!\w)(Россия|Беларусь|г\.\s?[А-Яа-яЁё]+|г\.[-]?\s?[А-Яа-яЁё]+|город\s?[А-Яа-яЁё]+|ул\.\s?[А-Яа-яЁё]+|улица\s?[А-Яа-яЁё]+|пер\.\s?[А-Яа-яЁё]+|[А-Яа-яЁё]+[-\s]?пер\.|переулок\s?[А-Яа-яЁё]+|д\.-?\s?\d+|дом\s?\d+|кв\.-?\s?\d+|квартира\s?\d+)",
                re.VERBOSE),
            "reg_num": re.compile(r"(?<!\w)\d{2}[-\s]?\d{3}[-\s]?\d{3}(?!\w)", re.VERBOSE),
            "diploma": re.compile(r"(?<!\w)ДК[-\s]?\d{8}\b|[А-Я]{2}[-\s]?\d{8}\b", re.VERBOSE),
        }

        print("Current mask type:", self.mask_type)
        text1 = text
        if self.mask_type == Mask.maskType:
            text = self.apply_mask(text, patterns, "***")
            return text, text == text1, text1
        elif self.mask_type == Mask.maskType2:
            text = self.apply_mask(text, patterns, "")
            return text, text == text1, text1
        elif self.mask_type == Mask.maskType3:
            masked_text = self.apply_mask(text, patterns, "***")
            return masked_text, (masked_text != text), text1

    def apply_mask(self, text, patterns, replacement):
        for pattern in patterns.values():
            text = pattern.sub(replacement, text)
        return text


# Пример использования
async def main():
    masking = Masking()

    print(masking is Masking())  # Это должно вывести True, так как оба экземпляра должны быть одинаковыми

    example_text = "Контактный номер: +1(234) 567-8901, паспорт 1234 567890."

    # Первичное маскирование
    masked_text = masking.mask_data(example_text)
    print("Masked text (initial):", masked_text)

    # Изменяем тип маски

    # Маскирование после изменения типа
    masked_text_updated = masking.mask_data(example_text)
    print("Masked text (after change):", masked_text_updated)


if __name__ == "__main__":
    asyncio.run(main())
