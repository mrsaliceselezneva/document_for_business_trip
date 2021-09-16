import logging
import csv
from fpdf import FPDF
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from emoji import emojize

import settings

logging.basicConfig(filename="bot.log", level=logging.INFO, filemode="w")

personal_info = {"name": "Алиса", "surname": "Селезнёва", "patronymic": "Игоревна"}


def start(update, contex):
    update.message.reply_text('Привет! Я бот, который помогает генирировать документы. Начнём?')


def help(update, contex):
    update.message.reply_text("/start - запустить бота\n/help - получить список команд\n/document - создать документ\n")


def any_message(update, contex):
    text = update.message.text
    update.message.reply_text("Я не понимаю тебя. Напиши /help")


def get_name(update, contex):
    update.message.reply_text("Как тебя зовут?")
    name = 'q'


def create_document(update, contex):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, txt="имя", ln=1, align="C")
    pdf.cell(200, 20, txt="surname", ln=1, align="C")

    pdf.output("командировочный %s %s %s.pdf" % (
        personal_info["surname"], personal_info["name"][0], personal_info["patronymic"][0]))
    with open("командировочный %s %s %s.pdf" % (
            personal_info["surname"], personal_info["name"][0], personal_info["patronymic"][0]), 'rb') as f:
        update.message.reply_document(f)
    smile = emojize(settings.EMOJI[0], use_aliases=True)
    update.message.reply_text(f"Хорошего дня! {smile}")


def main():
    bot = Updater(settings.API_KEY, use_context=True)

    disp = bot.dispatcher
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(CommandHandler("document", create_document))
    disp.add_handler(MessageHandler(Filters.text, any_message))

    logging.info("bot has started")
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
