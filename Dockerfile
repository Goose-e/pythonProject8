version: '3.1'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - ./path/to/your/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"


