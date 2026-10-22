# lazy import telebot
# from config import TOKEN
#
# bot = telebot.TeleBot(token=TOKEN)
#
#
# # @bot.message_handler(commands=['start'])  # ② /start kelsa — shu funksiya
# # def start(message):
# #     bot.reply_to(message, "Salom! Men Ustudy botman 🤖")
# #
# #
# # @bot.message_handler(func=lambda m: True)  # ③ qolgan HAMMA xabar — shu funksiya
# # def echo(message):
# #
# #     print(message.text, "yozgan malumotimiz")
# #     print(message.chat.id, "bot va foydalanuvchi ortasidagi lichkani idsi")
# #     print(message.from_user.first_name, "foydalanuvchi first name boladi")
# #     print(message.from_user.id, "foydalanuvchi userni idsi")
# #     print(message.content_type, "foydalanuvchi yubirgan malumotni type")
# #     text = message.text
# #
# #     if str(message.text).isupper():
# #         bot.send_message(message.chat.id, message.text.lower())
# #     elif message.text.isdigit():
# #         bot.send_message(message.chat.id, "Raqam jonatdingiz")
# #     else:
# #         bot.send_message(message.chat.id, message.text)  # xabarni qaytarib yuboradi
# #
# # bot.infinity_polling()
#
# royxatlar = {}
#
#
# def royxat(message):
#     return royxatlar.setdefault(message.chat.id, [])
#
#
# @bot.message_handler(commands=['start', 'help'])
# def start(message):
#     bot.reply_to(message, "📝 ToDo bot\n/add matn — qo'shish\n/list — ro'yxat\n/done 0 — bajarildi\n/del 0 — o'chirish")
#
#
# @bot.message_handler(commands=['add'])
# def add(message):
#     matn = message.text.replace("/add", "", 1).strip()
#     if matn == "":
#         bot.reply_to(message, "Format: /add Dars qilish")
#         return
#     r = royxat(message)
#     r.append("[ ] " + matn)
#     bot.reply_to(message, f"✅ #{len(r) - 1} qo'shildi: {matn}")
#
#
# @bot.message_handler(commands=['list'])
# def royxatni_korsat(message):
#     r = royxat(message)
#     if len(r) == 0:
#         bot.reply_to(message, "Ro'yxat bo'sh. /add bilan qo'shing")
#         return
#     qatorlar = [f"#{i} {v}" for i, v in enumerate(r)]
#     bot.reply_to(message, "\n".join(qatorlar))
#
#
# @bot.message_handler(commands=['done', 'del'])
# def done_del(message):
#     try:
#         buyruq, raqam = message.text.split()
#         idx = int(raqam)
#         r = royxat(message)
#         if buyruq == "/done":
#             r[idx] = r[idx].replace("[ ]", "[x]", 1)
#             bot.reply_to(message, "✔️ Bajarildi")
#         else:
#             del r[idx]
#             bot.reply_to(message, f"🗑 #{idx} o'chirildi")
#     except (ValueError, IndexError):                # "x" son emas / #99 yo'q
#         bot.reply_to(message, "Format: /done 0  yoki  /del 0")
#
#
# @bot.message_handler(func=lambda m: True)
# def boshqa(message):
#     bot.reply_to(message, "Tushunmadim 🤔 /help")
#
#
# bot.infinity_polling()

import telebot
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
JADVAL = {"dushanba": "Python 15:00", "chorshanba": "Python 15:00", "juma": "Loyiha 15:00"}
SAVOL = ("Python'da ro'yxat qanday belgilanadi?", ["[ ]", "{ }", "( )"], 0)
anketa = {}

def asosiy_menyu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📅 Dars jadvali", "📝 Ro'yxatdan o'tish")
    markup.row("🧠 Test", "ℹ️ Yordam")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    ism = message.from_user.first_name
    bot.send_message(message.chat.id, f"Salom, <b>{ism}</b>! 👋\nMen <i>Ustudy</i> maktab botiman.\nBuyruqlar: /help",
                     parse_mode="HTML", reply_markup=asosiy_menyu())

@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda m: m.text == "ℹ️ Yordam")
def yordam(message):
    bot.reply_to(message, "/start — boshlash\n/jadval — dars jadvali\n/jadval juma — bitta kun\n/royxat — ro'yxatdan o'tish\n/test — mini test")

# ... jadval(), royxat() + ism_qabul() + yosh_qabul(), test() + javob() — yuqoridagi bo'limlardagi kodlar ...

@bot.message_handler(func=lambda m: m.text == "📅 Dars jadvali")
def jadval(message):
    bot.reply_to(message, )

@bot.message_handler(content_types=['photo'])
def rasm(message):
    bot.reply_to(message, "📷 Rasm qabul qilindi! Chiroyli ekan.")

@bot.message_handler(content_types=['sticker'])
def stiker(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)

@bot.message_handler(content_types=['location'])
def joy(message):
    lat, lon = message.location.latitude, message.location.longitude
    bot.reply_to(message, f"📍 Siz shu yerdasiz: {lat:.4f}, {lon:.4f}")
    bot.send_location(message.chat.id, 41.3111, 69.2797)

@bot.message_handler(func=lambda m: True)                   # ENG OXIRIDA
def boshqa(message):
    bot.reply_to(message, "Tushunmadim 🤔 /help yoki tugmalardan foydalaning")

bot.infinity_polling()