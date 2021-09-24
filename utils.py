from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard():
    # , KeyboardButton("Магия", request_contact=True)
    return ReplyKeyboardMarkup([["Создать командировочный"]])


#def yes_no_button():
#    inline_kb_full = InlineKeyboardMarkup([[InlineKeyboardButton("Да", text="Yes"),
#                                            InlineKeyboardButton("Нет", text="No")]])
#    return inline_kb_full

def yes_no_keyboard():
    return ReplyKeyboardMarkup([["Да", "Нет"]])

def start(update, contex):
    update.message.reply_text("Привет! Я бот, который помогает генирировать документы. Начнём?",
                              reply_markup=main_keyboard())


def help(update, contex):
    update.message.reply_text("/start - запустить бота\n/help - получить список команд\n/document - создать документ\n",
                              reply_markup=main_keyboard())


def any_message(update, contex):
    text = update.message.text
    update.message.reply_text("Я не понимаю тебя. Напиши /help", reply_markup=main_keyboard())
