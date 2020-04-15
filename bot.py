import telebot
from variables import *
import pf

start_mess = "Привет!\nЭтот бот поможет тебе выделить все песни, упоминающиеся" \
             " в статье о музыке. Пока что бот работает не со всеми сайтами, однако " \
             "он хорошо работает с такими крупными проектами, как портал Pitchfork " \
             "и Википедией."
help_mess = "Просто введи адрес страницы, и я верну тебе список всех песен оттуда. " \
            "Если на какой-то странице ничего не находится, то, возможно, я просто пока " \
            "не умею обрабатывать такие страницы."

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, start_mess)

@bot.message_handler(commands=['help'])
def start_handler(message):
    bot.send_message(message.from_user.id, help_mess)

@bot.message_handler(content_types=['text'])
def send_songs(message):
    bot.send_message(message.chat.id, "Пожалуйста, подождите, это может занять пару минут.")
    ans = ""
    try:
        ans = pf.check_site(message.text)
    except Exception:
        bot.send_message(message.chat.id, "Простите, какие-то неполадки, попробуйте ещё раз позже.")
    if len(ans) == 0:
        bot.send_message(message.chat.id, "На этой странице нет упоминаний песен.")
    else:
        bot.send_message(message.chat.id, pf.check_site(message.text))

bot.polling()
