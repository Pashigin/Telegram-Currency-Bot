import telebot
import requests
import os
from dotenv import load_dotenv
from currency_sharaf import get_rates_from_sharaf

# Загружаем переменные окружения из файла .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN can not be None")

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


# Создание клавиатуры
def create_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Проверить оф. курс USD"))
    markup.add(telebot.types.KeyboardButton("Проверить оф. курс EUR"))
    markup.add(telebot.types.KeyboardButton("Проверить курс в Sharaf Exchange"))
    return markup


# Функция для получения курса валют из API
def get_exchange_rate(currency_code: str):
    try:
        response = requests.get(f"https://open.er-api.com/v6/latest/{currency_code}")
        data = response.json()
        return data["rates"]["AED"]
    except Exception as e:
        print(f"error getting the rate for {currency_code}: {e}")
        return None


# Обработчик команд /start и /help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Я бот, который проверяет курс валют ОАЭ. Если хотите проверить, нажмите на любую кнопку ниже.",
        reply_markup=create_markup(),
    )


# Проверка курса валюты USD
@bot.message_handler(func=lambda message: message.text == "Проверить оф. курс USD")
def check_usd_currency(message):
    aed_rate = get_exchange_rate("USD")
    if aed_rate:
        bot.send_message(message.chat.id, f"Текущий курс: 1 USD = {aed_rate} AED")
    else:
        bot.send_message(message.chat.id, "Ошибка при получении курса USD.")


# Проверка курса валюты EUR
@bot.message_handler(func=lambda message: message.text == "Проверить оф. курс EUR")
def check_eur_currency(message):
    aed_rate = get_exchange_rate("EUR")
    if aed_rate:
        bot.send_message(message.chat.id, f"Текущий курс: 1 EUR = {aed_rate} AED")
    else:
        bot.send_message(message.chat.id, "Ошибка при получении курса EUR.")


# Проверка курса валюты USD и EUR в Sharaf Exchange
@bot.message_handler(
    func=lambda message: message.text == "Проверить курс в Sharaf Exchange"
)
def check_currency_sharaf(message):
    rates = get_rates_from_sharaf()

    usd_rate = rates.get("USD")
    eur_rate = rates.get("EUR")

    if usd_rate is None or eur_rate is None:
        bot.send_message(
            message.chat.id, "Не удалось получить курс валют. (ошибка в программе)"
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=(
                "Покупают:\n"
                f"1 USD = {usd_rate[0]:.6f} AED\n"
                f"1 EUR = {eur_rate[0]:.6f} AED\n\n"
                "Продают:\n"
                f"1 USD = {usd_rate[1]:.6f} AED\n"
                f"1 EUR = {eur_rate[1]:.6f} AED"
            ),
        )


# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(
        message.chat.id,
        text="Простите, не понял команду. Используйте кнопки снизу, чтобы продолжить",
    )


# Запуск бота
bot.infinity_polling()
