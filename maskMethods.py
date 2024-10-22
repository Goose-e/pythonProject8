import re
from enumMask import Mask


class Masking():
    @staticmethod
    def maskData(text, maskType):
        # 1. Мобильные телефоны
        phone_pattern = re.compile(r"""
            (?<!\w)                            # Убедимся, что перед номером нет букв
            (\+?\d{1,3}[-\s]?)?                # Код страны
            \(?\d{3}\)?[-\s]?                  # Код оператора
            \d{1,3}[-\s]?\d{1,2}[-\s]?\d{2,3}  # Основной номер
            (?!\w)                             # Убедимся, что после номера нет букв
        """, re.VERBOSE)

        passport_pattern = re.compile(r"""
            \b\d{4}[-\s]?\d{6}\b|              # Номер паспорта
            \b[А-Я]{2}\d{7}\b                   # Белорусские номера паспортов
        """, re.VERBOSE)

        # 3. Номера банковских карт
        card_pattern = re.compile(r"""
            (?<!\w)                            # Убедимся, что перед номером нет букв
            (?:\d{4}[-\s]?){3}\d{4}\b|         # Формат: 1234-5678-9012-3456 или 1234 5678 9012 3456
            \d{16}\b                            # Формат: 1234567890123456
        """, re.VERBOSE)

        # 4. Номера счетов
        account_pattern = re.compile(r"""
            (?<!\w)                            # Убедимся, что перед номером нет букв
            (?:\d{4}[-\s]?){4}\d{4}\b         # Номер счета
        """, re.VERBOSE)

        # 5. Даты рождения
        date_pattern = re.compile(r"""
            (\b\d{2}[-./]\d{2}[-./]\d{4}\b)|    # ДД.ММ.ГГГГ
            (\b\d{4}[-./]\d{2}[-./]\d{2}\b)|    # ГГГГ.ММ.ДД
            (\b\d{2}\s\w{3,}\s\d{4}\b)          # ДД МЕСЯЦ ГГГГ
        """, re.VERBOSE)

        # 6. Имена и фамилии
        name_pattern = re.compile(r"""
            (?<!\w)                            # Убедимся, что перед именем нет букв
            (\b[A-ZА-ЯЁ][a-zа-яё]+\s[A-ZА-ЯЁ][a-zа-яё]+\b)|        # Имя Фамилия
            (\b[A-ZА-ЯЁ]\.\s[A-ZА-ЯЁ][a-zа-яё]+\b)|                # И. Фамилия
            (\b[A-ZА-ЯЁ]\.\s[A-ZА-ЯЁ]\.\s[A-ZА-ЯЁ][a-zа-яё]+\b)    # И. О. Фамилия
        """, re.VERBOSE)

        # 7. Адреса
        address_pattern = re.compile(r"""
            (?<!\w)                            # Убедимся, что перед адресом нет букв
            (Россия|г\.\s?[А-Яа-яЁё]+|г[-]?\s?[А-Яа-яЁё]+|ул\.\s?[А-Яа-яЁё]+|пер\.\s?[А-Яа-яЁё]+|д\.\s?\d+|кв\.\s?\d+|дом\s?\d+)
        """, re.VERBOSE)

        # 8. Регистрационные номера
        reg_num_pattern = re.compile(r"""
            (?<!\w)                            # Убедимся, что перед номером нет букв
            \d{2}[-\s]?\d{3}[-\s]?\d{3}(?!\w)  # Регистрационный номер
        """, re.VERBOSE)

        # 9. Номера дипломов
        diploma_pattern = re.compile(r"""
            (?<!\w)                            # Убедимся, что перед номером нет букв
            ДК[-\s]?\d{8}\b|                   # Диплом в формате ДК00123456 или ДК 00123456
            [А-Я]{2}[-\s]?\d{8}\b               # Другие форматы дипломов
        """, re.VERBOSE)
        if maskType == 1:
            print(maskType)
            text1 = text
            text = phone_pattern.sub("***", text)
            text = passport_pattern.sub("***", text)
            text = card_pattern.sub("***", text)
            text = account_pattern.sub("***", text)
            text = date_pattern.sub("***", text)
            text = name_pattern.sub("***", text)
            text = address_pattern.sub("***", text)
            text = reg_num_pattern.sub("***", text)
            text = diploma_pattern.sub("***", text)

            def maskRemainingDigits(text):
                text = re.sub(r'\b\d{4,}\b', '***', text)
                text = re.sub(r'\*\*\*\d{2,4}', '***', text)
                return text

            text = maskRemainingDigits(text)

            return text, (text1 == text), text1
        elif maskType == 2:
            print(maskType)
            text1 = text
            text = phone_pattern.sub("", text)
            text = passport_pattern.sub("", text)
            text = card_pattern.sub("", text)
            text = account_pattern.sub("", text)
            text = date_pattern.sub("", text)
            text = name_pattern.sub("", text)
            text = address_pattern.sub("", text)
            text = reg_num_pattern.sub("", text)
            text = diploma_pattern.sub("", text)

            def maskRemainingDigits(text):
                text = re.sub(r'\b\d{4,}\b', '', text)
                text = re.sub(r'\*\*\*\d{2,4}', '', text)
                return text

            text = maskRemainingDigits(text)

            return text, (text1 == text), text1
        elif maskType == 3:
            text1 = text
            text = phone_pattern.sub("***", text)
            text = passport_pattern.sub("***", text)
            text = card_pattern.sub("***", text)
            text = account_pattern.sub("***", text)
            text = date_pattern.sub("***", text)
            text = name_pattern.sub("***", text)
            text = address_pattern.sub("***", text)
            text = reg_num_pattern.sub("***", text)
            text = diploma_pattern.sub("***", text)
            return text, (text1 == text), text1

            def maskRemainingDigits(text):
                text = re.sub(r'\b\d{4,}\b', '***', text)
                text = re.sub(r'\*\*\*\d{2,4}', '***', text)
                return text

            text = maskRemainingDigits(text)
            if text1 != text:
                return False
            else:
                return text, (text1 == text), text1
