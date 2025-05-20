import asyncio
import os
from functools import partial

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot, telebot

from get_api_data import check_currency_sharaf, check_official_currency

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN can not be None")

bot = AsyncTeleBot(TELEGRAM_TOKEN)


# Клавиатура
def create_markup():
    return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
        "USD → AED",
        "EUR → AED",
        "Курс обменника\nUSD → AED",
        "Курс обменника\nEUR → AED",
        "Проверить любую валюту",
        "Проверить в обменнике → AED",
    )


# Состояния пользователей
user_states = {}


# Приветствие
@bot.message_handler(commands=["start", "help"])
async def send_welcome(message):
    name = message.from_user.first_name or "Друг"
    await bot.send_message(
        message.chat.id,
        (
            f"Привет, {name}! 👋\n\n"
            "Я бот, который показывает курс дирхама ОАЭ 🇦🇪\n"
            "Данные берутся из официального источника и <a href='https://sharafexchange.ae'>Sharaf Exchange</a> 💰\n"
            "Выбери нужную команду ниже 👇\n\n"
            "Для связи: @pashigin"
        ),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=create_markup(),
    )


# Обработчики кнопок
button_handlers = {
    "USD → AED": partial(check_official_currency, "USD"),
    "EUR → AED": partial(check_official_currency, "EUR"),
    "Курс обменника\nUSD → AED": partial(check_currency_sharaf, "USD"),
    "Курс обменника\nEUR → AED": partial(check_currency_sharaf, "EUR"),
}


# Обработчик кнопок со стандартными валютами
@bot.message_handler(func=lambda msg: msg.text in button_handlers)
async def handle_currency_buttons(message):
    result = await button_handlers[message.text]()
    await bot.send_message(message.chat.id, result, parse_mode="HTML")


# Ввод пользователем произвольной оф валюты
@bot.message_handler(func=lambda msg: msg.text == "Проверить любую валюту")
async def start_custom_currency_check(message):
    user_states[message.from_user.id] = {"step": "base"}
    await bot.send_message(message.chat.id, "Введи базовую валюту (например, USD):")


# Ввод пользователем произвольной валюты к дирхаму в обменника
@bot.message_handler(func=lambda msg: msg.text == "Проверить в обменнике → AED")
async def ask_sharaf_currency(message):
    user_states[message.from_user.id] = {"step": "custom_sharaf"}
    await bot.send_message(message.chat.id, "Введи валюту к дирхаму (например, USD):")


@bot.message_handler(func=lambda msg: msg.from_user.id in user_states)
async def handle_states(message):
    user_id = message.from_user.id
    state = user_states[user_id]
    text = message.text.strip().upper()

    if len(text) != 3 or not text.isalpha():
        await bot.send_message(
            message.chat.id, "Введи корректный код валюты (3 буквы, например, USD)."
        )
        return

    step = state["step"]

    if step == "base":
        state.update({"step": "target", "base": text})
        await bot.send_message(
            message.chat.id, "Теперь введи целевую валюту (например, AED):"
        )

    elif step == "target":
        base = state["base"]
        target = text
        del user_states[user_id]
        result = await check_official_currency(base, target)
        await bot.send_message(message.chat.id, result, parse_mode="HTML")

    elif step == "custom_sharaf":
        del user_states[user_id]
        result = await check_currency_sharaf(text)
        await bot.send_message(message.chat.id, result, parse_mode="HTML")


# Ответ на любое другое сообщение
@bot.message_handler(func=lambda msg: True)
async def echo_all(message):
    await bot.send_message(
        message.chat.id,
        "Прости, не понял команду. Используй кнопки меню 👇",
        reply_markup=create_markup(),
    )


# Запуск бота
if __name__ == "__main__":
    asyncio.run(bot.polling())
