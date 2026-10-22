import json
from datetime import datetime
import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
from config import TOKEN, ADMIN_ID

bot = telebot.TeleBot(TOKEN)

FAYL = "royxat.json"

JADVAL = {
    "dushanba": [
        ("13:00–14:30", "IDS", "A101 PC Lab", "A.Nurullaev"),
        ("14:30–16:30", "PP", "B201", "M.Asranov"),
    ],
    "seshanba": [
        ("12:30–14:00", "IDS", "B102 PC Lab", "A.Nurullaev"),
        ("14:00–16:00", "PP", "A607", "M.Asranov"),
        ("16:00–18:00", "Math 2", "B202", "O.Farmonov"),
    ],
    "chorshanba": [
        ("14:30–16:30", "PP", "B209", "M.Asranov"),
    ],
    "payshanba": [
        ("12:30–14:30", "Math 2", "B306", "O.Farmonov"),
        ("14:30–16:30", "TE", "A705", "P.Musurmanova"),
    ],
    "juma": [
        ("16:00–18:00", "Math 2", "A501", "O.Farmonov"),
    ],
}

TESTLAR = [
    ("Python'da ro'yxat (list) qanday belgilanadi?", ["[ ]", "{ }", "( )"], 0),
    ("Ekranga matn chiqaradigan funksiya qaysi?", ["input()", "print()", "len()"], 1),
    ("Python'da lug'at (dict) qanday belgilanadi?", ["[ ]", "{ }", "( )"], 1),
]

anketa = {}
test_holat = {}


def asosiy_menyu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📅 Dars jadvali", "📝 Ro'yxatdan o'tish")
    markup.row("🧠 Test", "ℹ️ Yordam")
    return markup


def royxatni_oqi():
    try:
        with open(FAYL, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def royxatni_yoz(data):
    with open(FAYL, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def safe_edit(call, matn, markup=None):
    try:
        bot.edit_message_text(
            matn,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=markup,
        )
    except ApiTelegramException as e:
        if "message is not modified" in str(e):
            print("Matn o'zgarmadi, e'tiborsiz qoldirildi:", e)
        else:
            raise


@bot.message_handler(commands=['start'])
def start(message):
    ism = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f"Salom, <b>{ism}</b>! 👋\nMen <i>Ustudy</i> maktab botiman.\nBuyruqlar: /help",
        parse_mode="HTML",
        reply_markup=asosiy_menyu(),
    )


@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda m: m.text == "ℹ️ Yordam")
def yordam(message):
    bot.reply_to(
        message,
        "/start — boshlash\n"
        "/jadval — dars jadvali\n"
        "/jadval juma — bitta kun\n"
        "/royxat — ro'yxatdan o'tish\n"
        "/id — chat_id ni bilish\n"
        "/royxatlar — ro'yxatdan o'tganlar (faqat admin)\n"
    )


@bot.message_handler(commands=['id'])
def chat_id_ber(message):
    bot.reply_to(message, f"chat_id: {message.chat.id}")


def kun_matni(kun):
    qatorlar = [f"<b>{kun.capitalize()}</b>"]
    for vaqt, fan, xona, oqituvchi in JADVAL[kun]:
        qatorlar.append(f"🕐 {vaqt} — <b>{fan}</b> ({xona}, {oqituvchi})")
    return "\n".join(qatorlar)


@bot.message_handler(commands=['jadval'])
@bot.message_handler(func=lambda m: m.text == "📅 Dars jadvali")
def jadval(message):
    qismlar = message.text.split()
    if len(qismlar) > 1 and message.text.startswith("/"):
        kun = qismlar[1].lower()
        if kun not in JADVAL:
            bot.reply_to(message, "Bunday kun yo'q. Masalan: /jadval juma")
            return
        bot.send_message(message.chat.id, kun_matni(kun), parse_mode="HTML")
        return
    matn = "📅 <b>Dars jadvali</b>\n\n" + "\n\n".join(kun_matni(k) for k in JADVAL)
    bot.send_message(message.chat.id, matn, parse_mode="HTML")


def bekor_qilindimi(message):
    if message.text and message.text.startswith("/"):
        anketa.pop(message.chat.id, None)
        bot.send_message(
            message.chat.id,
            "Ro'yxatdan o'tish bekor qilindi.",
            reply_markup=asosiy_menyu(),
        )
        return True
    return False


@bot.message_handler(commands=['royxat'])
@bot.message_handler(func=lambda m: m.text == "📝 Ro'yxatdan o'tish")
def royxat(message):
    msg = bot.send_message(
        message.chat.id,
        "Ismingiz nima? (bekor qilish uchun /bekor)",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    bot.register_next_step_handler(msg, ism_qabul)


def ism_qabul(message):
    if bekor_qilindimi(message):
        return
    if not message.text or len(message.text.strip()) < 2:
        msg = bot.send_message(message.chat.id, "Iltimos, ismingizni matn bilan yozing:")
        bot.register_next_step_handler(msg, ism_qabul)
        return
    anketa[message.chat.id] = {"ism": message.text.strip()}
    msg = bot.send_message(message.chat.id, "Yoshingiz nechada?")
    bot.register_next_step_handler(msg, yosh_qabul)


def telefon_so_ra(chat_id, matn):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True))
    msg = bot.send_message(chat_id, matn, reply_markup=markup)
    bot.register_next_step_handler(msg, telefon_qabul)


def yosh_qabul(message):
    if bekor_qilindimi(message):
        return
    if not message.text or not message.text.strip().isdigit() or not 5 <= int(message.text) <= 100:
        msg = bot.send_message(message.chat.id, "Yoshni raqam bilan yozing (5–100):")
        bot.register_next_step_handler(msg, yosh_qabul)
        return
    if message.chat.id not in anketa:
        bot.send_message(message.chat.id, "Jarayon uzildi, /royxat dan qaytadan boshlang.")
        return
    anketa[message.chat.id]["yosh"] = int(message.text)
    telefon_so_ra(message.chat.id, "Endi telefon raqamingizni pastdagi tugma orqali yuboring 👇")


def telefon_qabul(message):
    if bekor_qilindimi(message):
        return
    if not message.contact or message.contact.user_id != message.from_user.id:
        telefon_so_ra(message.chat.id, "Iltimos, tugmani bosing (o'zingizning raqamingiz):")
        return
    malumot = anketa.pop(message.chat.id, None)
    if malumot is None:
        bot.send_message(message.chat.id, "Jarayon uzildi, /royxat dan qaytadan boshlang.")
        return

    yozuv = {
        "chat_id": message.chat.id,
        "username": message.from_user.username,
        "ism": malumot["ism"],
        "yosh": malumot["yosh"],
        "telefon": message.contact.phone_number,
        "vaqt": datetime.now().isoformat(timespec="seconds"),
    }
    data = royxatni_oqi()
    # bir kishi qayta o'tsa — yangilaymiz, dublikat qilmaymiz
    data = [d for d in data if d.get("chat_id") != message.chat.id]
    data.append(yozuv)
    royxatni_yoz(data)

    bot.send_message(
        message.chat.id,
        f"✅ Rahmat, <b>{yozuv['ism']}</b>! Ro'yxatdan o'tdingiz.",
        parse_mode="HTML",
        reply_markup=asosiy_menyu(),
    )


@bot.message_handler(commands=['royxatlar'])
def royxatlar(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "⛔ Bu buyruq faqat admin uchun.")
        return
    data = royxatni_oqi()
    if not data:
        bot.reply_to(message, "Hozircha hech kim ro'yxatdan o'tmagan.")
        return
    qatorlar = [
        f"{n}. {d['ism']}, {d['yosh']} yosh, {d['telefon']}"
        for n, d in enumerate(data, 1)
    ]
    matn = f"Jami: {len(data)} ta\n\n" + "\n".join(qatorlar)
    for i in range(0, len(matn), 4000):
        bot.send_message(message.chat.id, matn[i:i + 4000])\

bot.infinity_polling()