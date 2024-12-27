import telebot
import requests
from currency_sharaf import get_rates_from_sharaf


bot = telebot.TeleBot("7847201576:AAEYASQu4Sp3XFf0uhzFDd4NkK_3Jv5hi58", parse_mode=None)

markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

markup.add(telebot.types.KeyboardButton("Проверить оф. курс доллара"))
markup.add(telebot.types.KeyboardButton("Проверить оф. курс евро"))
markup.add(telebot.types.KeyboardButton("Проверить курс в Sharaf Exchange"))


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Я бот, который проверяет курс валют ОАЭ. Если хотите проверить, нажмите на любую кнопку ниже.",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Проверить оф. курс доллара")
def check_usd_currency(message):
    try:
        # Используем API для получения курса
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        aed_rate = data["rates"]["AED"]
        bot.send_message(message.chat.id, f"Текущий курс: 1 USD = {aed_rate} AED")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при получении курса: {e}")


@bot.message_handler(func=lambda message: message.text == "Проверить оф. курс евро")
def check_eur_currency(message):
    try:
        # Используем API для получения курса
        response = requests.get("https://open.er-api.com/v6/latest/EUR")
        data = response.json()
        aed_rate = data["rates"]["AED"]
        bot.send_message(message.chat.id, f"Текущий курс: 1 EUR = {aed_rate} AED")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при получении курса: {e}")


@bot.message_handler(
    func=lambda message: message.text == "Проверить курс в Sharaf Exchange"
)
def check_currency_sharaf(message):
    try:
        rates = get_rates_from_sharaf()  # Получаем курс валют
        if isinstance(rates, dict):
            usd_rate = rates.get(
                "USD", ("Нет данных", "Нет данных")
            )  # Получаем курс USD
            eur_rate = rates.get(
                "EUR", ("Нет данных", "Нет данных")
            )  # Получаем курс EUR

            bot.send_message(
                chat_id=message.chat.id,
                text=(
                    "Покупают:\n"
                    f"1 USD = {usd_rate[0]} AED\n"
                    f"1 EUR = {eur_rate[0]} AED\n\n"
                    "Продают:\n"
                    f"1 USD = {usd_rate[1]} AED\n"
                    f"1 EUR = {eur_rate[1]} AED"
                ),
            )
        else:
            bot.send_message(message.chat.id, "Не удалось получить курс валют.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при получении курса: {e}")


@bot.message_handler(func=lambda message: message.text == "Ну ты и пиздабол")
def bad_message(message):
    bot.reply_to(
        message,
        text="Кто бы говорил, нахуй послан",
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(
        message.chat.id,
        text="Простите, не понял команду. Используйте кнопки снизу, чтобы продолжить",
    )


bot.infinity_polling()
