# Указываем базовый образ с Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /server

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt ./

# Обновление pip
RUN pip install --upgrade pip

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в рабочую директорию контейнера
COPY . .

# Открываем порты
EXPOSE 5010


# Запускаем приложение
CMD ["uvicorn", "servers.reverseServer1:servApp", "--host", "127.0.0.1", "--port", "5010", "--lifespan", "on"]
