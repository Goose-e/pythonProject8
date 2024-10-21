import re

maskType=1
class Masking():
    @staticmethod
    def maskData(text,type):
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
        if type==1:
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

            return text
        elif type==2:
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

            return text
        elif type ==3:
            checker=text
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
            if checker!=text:
                return False
            else:
                return text
    def changeMaskType(self, type):
        maskType=type


'''
test_texts = [
    "Меня зовут Анна Иванова, мой номер паспорта 4044-528828, а номер карты 5773-2909-7067-8674. Дата рождения: 25 MAY 1982.",
    "Мой номер телефона +375 29 888 98 87, а адрес: Россия, г. Сочи, Зеленый пер., д. 20, кв. 67.",
    "Телефоны: +375-888-98-87, 3758889887, (802) 946-45-54, 8 (029) 464-54-54.",
    "Номера паспортов: 4044 528828, 4044528828, 4044-528828, KM5557836.",
    "Номера карт: 5773 2909 7067 8674, 5773290970678674, 5773-2909-7067-8674.",
    "Номера счетов: 5091 8082 1000 0000 9484, 50918082100000009484, 5091-8082-1000-0000-9484.",
    "Дата рождения: 25.05.1982, 1982.05.25, 25 MAY 1982.",
    "Имена: Daniil Zabolotnyy, D. Zabolotnyy, D. L. Zabolotnyy.",
    "Адрес: Россия, г.-Сочи, Зеленый-пер., д.-20, кв.-67.",
    "Регистрационный номер: 53 245 089, 53245089.",
    "Номер диплома: ДК 00123456, ДК-00123456, ДК00123456."
]
'''
