from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from fpdf import FPDF
from emoji import emojize
import pandas
import time
from selenium import webdriver

from utils import main_keyboard, yes_no_keyboard
import settings

city_cod = {}


def read_city():
    global city_cod
    city_cod = pandas.read_excel("city_cod.xlsx")
    city = city_cod["city"].tolist()
    cod = city_cod["cod"].tolist()
    city_cod = {}
    for i in range(len(city)):
        city_cod[city[i]] = cod[i]
        city_cod[cod[i]] = city[i]
    return


def parsing(update, contex):
    url = settings.url + contex.user_data["form"]["city_from"] \
          + contex.user_data["form"]["date_from"][0] + contex.user_data["form"]["date_from"][1] \
          + contex.user_data["form"]["city_to"] \
          + contex.user_data["form"]["date_to"][0] + contex.user_data["form"]["date_to"][1] + "1"

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(7)
    containers = driver.find_elements_by_xpath("//*[@class='text_d1901f3']")
    compare = []
    for el in containers:
        if len(el.text) > 0 and el.text[-1] == '₽':
            compare.append(el.text[10:-1].split('\u2009')[0] + el.text[10:-1].split('\u2009')[1])

    driver.close()

    return compare[0]


def form_start(update, contex):
    smile = emojize(settings.EMOJI[0], use_aliases=True)
    update.message.reply_text(f"Начнём регистрацию{smile}! Для начала скажите вашу фамилию, имя и отчество",
                              reply_markup=main_keyboard())
    read_city()
    return "name"


def form_name(update, contex):
    user_name = update.message.text.split()
    if len(user_name) != 3:
        update.message.reply_text("Пожалуйста, введите фамилию, имя и отчество",
                                  reply_markup=main_keyboard())
        return "name"
    else:
        contex.user_data["form"] = {"name": user_name}
        update.message.reply_text("Из какого города вы отправляетесь?",
                                  reply_markup=main_keyboard())
        return "city_from"


def city_from(update, contex):
    global city_cod
    city_from = update.message.text
    if city_cod.get(city_from) is None:
        update.message.reply_text("Пожалуйста, проверьте название города",
                                  reply_markup=main_keyboard())
        return "city_from"
    else:
        contex.user_data["form"]["city_from"] = city_cod[city_from]
        update.message.reply_text("В какой город вы отправляетесь?",
                                  reply_markup=main_keyboard())
        return "city_to"


def city_to(update, contex):
    global city_cod
    city_to = update.message.text
    if city_cod.get(city_to) is None:
        update.message.reply_text("Пожалуйста, проверьте название города",
                                  reply_markup=main_keyboard())
        return "city_to"
    else:
        contex.user_data["form"]["city_to"] = city_cod[city_to]
        update.message.reply_text("Теперь введите дату вылета из города %s в формате ДД.ММ" %
                                  city_cod[contex.user_data["form"]["city_from"]],
                                  reply_markup=main_keyboard())
        return "date_from"


def date_from(update, contex):
    date_from = update.message.text
    if not (len(date_from.split('.')) == 2 and len(date_from.split('.')[0]) < 3 and len(date_from.split('.')[1]) < 3
            and date_from.split('.')[0].isdigit() and date_from.split('.')[1].isdigit()
            and 0 < int(date_from.split('.')[1]) < 13):
        update.message.reply_text("Пожалуйста, проверьте дату отправления",
                                  reply_markup=main_keyboard())
        return "date_from"
    else:
        date_from = date_from.split('.')
        date_from[0] = '0' * (2 - len(date_from[0])) + date_from[0]
        date_from[1] = '0' * (2 - len(date_from[1])) + date_from[1]
        contex.user_data["form"]["date_from"] = date_from
        update.message.reply_text("Теперь введите дату вылета из города %s в формате ДД.ММ" %
                                  city_cod[contex.user_data["form"]["city_to"]],
                                  reply_markup=main_keyboard())
        return "date_to"


def date_to(update, contex):
    date_to = update.message.text
    if not (len(date_to.split('.')) == 2 and len(date_to.split('.')[0]) < 3 and len(date_to.split('.')[1]) < 3
            and date_to.split('.')[0].isdigit() and date_to.split('.')[1].isdigit()
            and 0 < int(date_to.split('.')[1]) < 13):
        update.message.reply_text("Пожалуйста, проверьте дату отправления",
                                  reply_markup=main_keyboard())
        return "date_to"
    else:
        date_to = date_to.split('.')
        date_to[0] = '0' * (2 - len(date_to[0])) + date_to[0]
        date_to[1] = '0' * (2 - len(date_to[1])) + date_to[1]
        contex.user_data["form"]["date_to"] = date_to
        update.message.reply_text("Проверяю наличие рейсов...", reply_markup=ReplyKeyboardRemove())
        contex.user_data["form"]["cost"] = parsing(update, contex)
        if len(contex.user_data["form"]["cost"]) == 0:
            update.message.reply_text("Упс... У меня не получилось найти рейсы... Попробуйте другие даты",
                                      reply_markup=main_keyboard())
            return ConversationHandler.END
        else:
            update.message.reply_text("Рейсы найдены! Вам нужен pdf файл?", reply_markup=yes_no_keyboard())
            return "form_yes_no"


def form_yes_no(update, contex):
    text = update.message.text
    print(text)
    if text == "Нет":
        smile = emojize(settings.EMOJI[0], use_aliases=True)
        update.message.reply_text(f"Хорошего дня! {smile}",
                                  reply_markup=main_keyboard())
    else:
        update.message.reply_text("Сейчас вышлю pdf", reply_markup=ReplyKeyboardRemove())
        time.sleep(3)
        create_document(update, contex)
    return ConversationHandler.END


def create_document(update, contex):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, txt="Командировочный сотрудника %s %s %s." % (contex.user_data["form"]["name"][0],
                                                                    contex.user_data["form"]["name"][1],
                                                                    contex.user_data["form"]["name"][2]),
             ln=1, align="C")
    pdf.cell(160, 20,
             txt="Вылетает из города %s в город %s %s. Обратно %s." % (city_cod[contex.user_data["form"]["city_from"]],
                                                                       city_cod[contex.user_data["form"]["city_to"]],
                                                                       contex.user_data["form"]["date_from"][0] + "." +
                                                                       contex.user_data["form"]["date_from"][1],
                                                                       contex.user_data["form"]["date_to"][0] + "." +
                                                                       contex.user_data["form"]["date_to"][1]),
             ln=2, align="C")
    pdf.cell(170, 30, txt="Цена билета туда-обратно: %s рублей." % contex.user_data["form"]["cost"], ln=1, align="C")

    pdf.output("командировочный %s %s %s.pdf" % (contex.user_data["form"]["name"][0],
                                                 contex.user_data["form"]["name"][1][0],
                                                 contex.user_data["form"]["name"][2][0]))
    with open("командировочный %s %s %s.pdf" % (
            contex.user_data["form"]["name"][0], contex.user_data["form"]["name"][1][0],
            contex.user_data["form"]["name"][2][0]), 'rb') as f:
        update.message.reply_document(f, reply_markup=main_keyboard())
    smile = emojize(settings.EMOJI[0], use_aliases=True)
    update.message.reply_text(f"Хорошего дня! {smile}")
    return
