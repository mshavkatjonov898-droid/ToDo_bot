lazy import telebot
from config import TOKEN

bot = telebot.TeleBot(token=TOKEN)


# @bot.message_handler(commands=['start'])  # ② /start kelsa — shu funksiya
# def start(message):
#     bot.reply_to(message, "Salom! Men Ustudy botman 🤖")
#
#
# @bot.message_handler(func=lambda m: True)  # ③ qolgan HAMMA xabar — shu funksiya
# def echo(message):
#
#     print(message.text, "yozgan malumotimiz")
#     print(message.chat.id, "bot va foydalanuvchi ortasidagi lichkani idsi")
#     print(message.from_user.first_name, "foydalanuvchi first name boladi")
#     print(message.from_user.id, "foydalanuvchi userni idsi")
#     print(message.content_type, "foydalanuvchi yubirgan malumotni type")
#     text = message.text
#
#     if str(message.text).isupper():
#         bot.send_message(message.chat.id, message.text.lower())
#     elif message.text.isdigit():
#         bot.send_message(message.chat.id, "Raqam jonatdingiz")
#     else:
#         bot.send_message(message.chat.id, message.text)  # xabarni qaytarib yuboradi
#
# bot.infinity_polling()

royxatlar = {}                         # chat_id → ro'yxat (har kimga o'ziniki)


def royxat(message):
    return royxatlar.setdefault(message.chat.id, [])   # yo'q bo'lsa bo'sh ro'yxat yaratadi


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, "📝 ToDo bot\n/add matn — qo'shish\n/list — ro'yxat\n/done 0 — bajarildi\n/del 0 — o'chirish")


@bot.message_handler(commands=['add'])
def add(message):
    matn = message.text.replace("/add", "", 1).strip()     # "/add Dars qilish" → "Dars qilish"
    if matn == "":
        bot.reply_to(message, "Format: /add Dars qilish")
        return
    r = royxat(message)
    r.append("[ ] " + matn)
    bot.reply_to(message, f"✅ #{len(r) - 1} qo'shildi: {matn}")   # oxirgi element raqami


@bot.message_handler(commands=['list'])
def royxatni_korsat(message):
    r = royxat(message)
    if len(r) == 0:
        bot.reply_to(message, "Ro'yxat bo'sh. /add bilan qo'shing")
        return
    qatorlar = [f"#{i} {v}" for i, v in enumerate(r)]   # "#0 [ ] Dars qilish"
    bot.reply_to(message, "\n".join(qatorlar))


@bot.message_handler(commands=['done', 'del'])
def done_del(message):
    try:
        buyruq, raqam = message.text.split()       # "/done 0"
        idx = int(raqam)
        r = royxat(message)
        if buyruq == "/done":
            r[idx] = r[idx].replace("[ ]", "[x]", 1)       # "[ ] Dars" → "[x] Dars"
            bot.reply_to(message, "✔️ Bajarildi")
        else:
            del r[idx]
            bot.reply_to(message, f"🗑 #{idx} o'chirildi")
    except (ValueError, IndexError):                # "x" son emas / #99 yo'q
        bot.reply_to(message, "Format: /done 0  yoki  /del 0")


@bot.message_handler(func=lambda m: True)
def boshqa(message):
    bot.reply_to(message, "Tushunmadim 🤔 /help")


bot.infinity_polling()