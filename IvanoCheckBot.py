import asyncio
import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot, telebot

from get_api_data import check_currency_sharaf, check_official_currency

# Загружаем переменные окружения из файла .env
load_dotenv()

api_url = os.getenv("OFFICIAL_API_URL")
sharaf_api_url = os.getenv("SHARAF_API_URL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN can not be None")

# Инициализация асинхронного бота
bot = AsyncTeleBot(TELEGRAM_TOKEN)


# Создание клавиатуры
def create_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Проверить оф. курс USD"))
    markup.add(telebot.types.KeyboardButton("Проверить оф. курс EUR"))
    markup.add(telebot.types.KeyboardButton("Sharaf Exchange AED/USD"))
    markup.add(telebot.types.KeyboardButton("Sharaf Exchange AED/EUR"))
    return markup


# Обработчик команд /start и /help
@bot.message_handler(commands=["start", "help"])
async def send_welcome(message):
    await bot.send_message(
        message.chat.id,
        "Здравствуйте! Я бот, который проверяет курс валют ОАЭ. Если хотите проверить, нажмите на любую кнопку ниже.",
        reply_markup=create_markup(),
    )


# Проверка курса валюты USD
@bot.message_handler(func=lambda message: message.text == "Проверить оф. курс USD")
async def check_usd_currency(message):
    result = await check_official_currency("USD")
    await bot.send_message(message.chat.id, result, parse_mode="HTML")


# Проверка курса валюты EUR
@bot.message_handler(func=lambda message: message.text == "Проверить оф. курс EUR")
async def check_eur_currency(message):
    result = await check_official_currency("EUR")
    await bot.send_message(message.chat.id, result, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == "Sharaf Exchange AED/USD")
async def check_usd_currency_sharaf(message):
    result = await check_currency_sharaf("USD")
    await bot.send_message(message.chat.id, result, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == "Sharaf Exchange AED/EUR")
async def check_eur_currency_sharaf(message):
    result = await check_currency_sharaf("EUR")
    await bot.send_message(message.chat.id, result, parse_mode="HTML")


# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
async def echo_all(message):
    await bot.send_message(
        message.chat.id,
        text="Простите, не понял команду. Используйте кнопки снизу, чтобы продолжить",
    )


# Запуск бота
if __name__ == "__main__":
    asyncio.run(bot.polling())
