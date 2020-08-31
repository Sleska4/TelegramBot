import config
import telebot
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    img = ['stic/AnimatedSticker.tgs', 'stic/AnimatedSticker1.tgs', 'stic/AnimatedSticker2.tgs',
           'stic/AnimatedSticker3.tgs', 'stic/AnimatedSticker4.tgs', 'stic/AnimatedSticker5.tgs',
           'stic/AnimatedSticker6.tgs',]
    img = open(img[random.randint(0, len(img)) - 1], 'rb')
    bot.send_sticker(message.chat.id, img)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    LIST = telebot.types.KeyboardButton("Список 🗒")
    ADD = telebot.types.KeyboardButton("Добавить 📌")
    DEL = telebot.types.KeyboardButton("Удалить 🗑")

    markup.add(LIST, ADD, DEL)

    hello_text = ["Привет, <b>{0.first_name}</b>.", "Во славу Первой Чувашской Империи", "Готов служить и повиноваться",
                  "памагите, наса держать адин чувашаский психа в падавали и нэ выпускадъ наз пака мы ни напижем "
                  "иму эта праграма", ]
    bot.send_message(message.chat.id, hello_text[random.randint(0,len(hello_text) - 1)].format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


def addF(message):
    add = message.text
    config.arr.append(add)
    bot.send_message(message.chat.id, 'Текст успешно добавлен')

@bot.message_handler(content_types=['text'])
def LIST(message):
    if message.chat.type == 'private':
        if message.text == 'Список 🗒':
            bot.send_message(message.chat.id, '\n'.join(config.arr))

        elif message.text == "Добавить 📌":
            add = bot.send_message(message.chat.id, 'Введите текст:')
            bot.register_next_step_handler(add, addF)





bot.polling(none_stop=True)