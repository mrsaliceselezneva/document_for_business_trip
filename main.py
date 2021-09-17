import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import create_document
import settings
from utils import start, help, any_message

logging.basicConfig(filename="bot.log", level=logging.INFO, filemode="w")


def main():
    bot = Updater(settings.API_KEY, use_context=True)

    disp = bot.dispatcher
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(CommandHandler("document", create_document))
    disp.add_handler(MessageHandler(Filters.regex("^(Создать командировочный)$"), create_document))
    # disp.add_handler(MessageHandler(Filters.location, users_coordinates))
    disp.add_handler(MessageHandler(Filters.text, any_message))

    logging.info("bot has started")
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
