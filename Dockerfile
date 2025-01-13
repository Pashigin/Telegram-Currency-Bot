FROM python:3.11-slim

# Установка системных зависимостей для Firefox
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libnspr4 \
    libgtk-3-0 \
    libx11-xcb1 \
    libdbus-glib-1-2 \
    libxtst6 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libfontconfig1 \
    libasound2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Playwright и Firefox
RUN pip install --no-cache-dir playwright \
    && playwright install-deps \
    && playwright install firefox

# Копирование файлов проекта
WORKDIR /app
COPY . /app

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска
CMD ["python", "IvanoCheckBot.py"]
