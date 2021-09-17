from fpdf import FPDF
from emoji import emojize

from utils import main_keyboard
import settings

personal_info = {"name": "Алиса", "surname": "Селезнёва", "patronymic": "Игоревна"}


def get_name(update, contex):
    update.message.reply_text("Как тебя зовут?", reply_markup=main_keyboard())


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
        update.message.reply_document(f, reply_markup=main_keyboard())
    smile = emojize(settings.EMOJI[0], use_aliases=True)
    update.message.reply_text(f"Хорошего дня! {smile}")


def users_coordinates(update, contex):
    coords = update.message.location
    smile = emojize(settings.EMOJI[0], use_aliases=True)
    update.message.reply_text(f"Я знаю, где ты сейчас {smile} {coords}", reply_markup=main_keyboard())
