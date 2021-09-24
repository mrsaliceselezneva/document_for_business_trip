import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import settings
from utils import start, help, any_message
from form import form_start, form_name, city_from, city_to, date_from, date_to, form_yes_no

logging.basicConfig(filename="bot.log", level=logging.INFO, filemode="w")


def main():
    bot = Updater(settings.API_KEY, use_context=True)

    disp = bot.dispatcher

    form = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("^(Создать командировочный)$"), form_start),
                      CommandHandler("document", form_start)],
        states={"name": [MessageHandler(Filters.text, form_name)],
                "city_from": [MessageHandler(Filters.text, city_from)],
                "city_to": [MessageHandler(Filters.text, city_to)],
                "date_from": [MessageHandler(Filters.text, date_from)],
                "date_to": [MessageHandler(Filters.text, date_to)],
                "form_yes_no": [MessageHandler(Filters.text, form_yes_no)]},
        fallbacks=[]
    )

    disp.add_handler(form)
    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("help", help))
    # disp.add_handler(CommandHandler("document", create_document))
    # disp.add_handler(MessageHandler(Filters.location, users_coordinates))
    disp.add_handler(MessageHandler(Filters.text, any_message))

    logging.info("bot has started")
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
