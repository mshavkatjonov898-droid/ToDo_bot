# lazy import telebot
# from config import TOKEN
#
# # bot = telebot.TeleBot(token=TOKEN)
# #
# # @bot.message_handler(commands=['start'])         # ② /start kelsa — shu funksiya
# # def start(message):
# #     bot.reply_to(message, "Salom! Men Ustudy botman 🤖")
# #
# # @bot.message_handler(func=lambda m: True)      # ③ qolgan HAMMA xabar — shu funksiya
# # def echo(message):
# #     bot.send_message(message.chat.id, message.text)  # xabarni qaytarib yuboradi
# #
# # bot.infinity_polling()
#
# bot = telebot.TeleBot(token=TOKEN)
#
#
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