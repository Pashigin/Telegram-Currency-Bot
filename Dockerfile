# Легковесный образ Python
FROM python:3.12-slim

# Установка Playwright и Chromium
RUN pip install --no-cache-dir playwright \
    && install --with-deps --only-shell chromium

# Создание рабочей директории
WORKDIR /app

# Копирование всего проекта
COPY . /app/

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска
CMD ["python", "IvanoCheckBot.py"]
