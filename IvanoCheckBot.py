import telebot


bot = telebot.TeleBot("7847201576:AAEYASQu4Sp3XFf0uhzFDd4NkK_3Jv5hi58", parse_mode=None)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(telebot.types.KeyboardButton("Проверить курс"))

    bot.send_message(
        message.chat.id,
        "Здравствуйте! Я бот, который проверяет курс валют ОАЭ. Если хотите проверить, нажмите на кнопку снизу",
        reply_markup=markup,
    )


bot.infinity_polling()
