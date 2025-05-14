# Легковесный образ Python
FROM python:3.13-slim

# Установка системных зависимостей (если нужно для библиотек, таких как psycopg2, lxml и т.д.)
RUN apt-get update

# Создание рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt /app/

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . /app/

# Команда запуска
CMD ["python", "IvanoCheckBot.py"]
