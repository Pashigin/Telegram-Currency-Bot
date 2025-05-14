import asyncio
import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot, telebot

from get_api_data import check_currency_sharaf, check_official_currency

# Загружаем переменные окружения из файла .env
load_dotenv()

api_url = os.getenv("OFFICIAL_API_URL")
sharaf_api_url = os.getenv("SHARAF_API_URL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_TEST2")

if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN can not be None")

# Инициализация асинхронного бота
bot = AsyncTeleBot(TELEGRAM_TOKEN)


# Создание клавиатуры
def create_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Оф. курс USD/AED"))
    markup.add(telebot.types.KeyboardButton("Оф. курс EUR/AED"))
    markup.add(telebot.types.KeyboardButton("Курс обменника USD/AED"))
    markup.add(telebot.types.KeyboardButton("Курс обменника EUR/AED"))
    return markup


# Обработчик команд /start и /help
@bot.message_handler(commands=["start", "help"])
async def send_welcome(message):
    await bot.send_message(
        message.chat.id,
        (
            "Здравствуйте!\nЯ бот, который проверяет и показывает курс Дирхама ОАЭ.\n"
            "Курсы валют взяты из официального источника и обменника <a href='https://sharafexchange.ae/'>Sharaf Exchange</a>.\n"
            "Пока реализованы только курс AED к USD и EUR.\n"
            "Если хотите проверить, нажмите на любую кнопку ниже 👇\n\n"
            "Для связи @pashigin"
        ),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=create_markup(),
    )


# Проверка курса валюты USD
@bot.message_handler(func=lambda message: message.text == "Оф. курс USD/AED")
async def check_usd_currency(message):
    result = await check_official_currency("USD")
    await bot.send_message(message.chat.id, result, parse_mode="HTML")


# Проверка курса валюты EUR
@bot.message_handler(func=lambda message: message.text == "Оф. курс EUR/AED")
async def check_eur_currency(message):
    result = await check_official_currency("EUR")
    await bot.send_message(message.chat.id, result, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == "Курс обменника USD/AED")
async def check_usd_currency_sharaf(message):
    result = await check_currency_sharaf("USD")
    await bot.send_message(message.chat.id, result, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == "Курс обменника EUR/AED")
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
