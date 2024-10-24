FROM postgres:16

# Копируем файл инициализации базы данных в контейнер
COPY init.sql /docker-entrypoint-initdb.d/

# Установка переменных окружения для базы данных
ENV POSTGRES_USER="postgres"
ENV POSTGRES_PASSWORD="Kolos213"
ENV POSTGRES_DB="postgres"

# Открываем порт PostgreSQL
EXPOSE 5432
