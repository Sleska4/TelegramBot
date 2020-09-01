import config
import telebot
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    img = open(config.img[random.randint(0, len(config.img)) - 1], 'rb')
    bot.send_sticker(message.chat.id, img)
    bot.send_message(message.chat.id, config.hello_text[random.randint(0,
    len(config.hello_text) - 1)].format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=config.menu())


def addF(message):
    add = message.text
    config.arr.append([add])
    print(config.arr)
    bot.send_message(message.chat.id, 'Текст успешно добавлен')
    time = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    time_add = telebot.types.KeyboardButton("Добавить ⏰")
    time_no = telebot.types.KeyboardButton("Нет, спасибо ❌")
    time.add(time_add, time_no)
    bot.send_message(message.chat.id, 'Хотите добавить время?'.format(message.from_user, bot.get_me()), reply_markup=time)


def time_add(message):
    time = message.text
    if time != "Нет, спасибо ❌":
        config.arr[len(config.arr) - 1].append(time)
        bot.send_message(message.chat.id, 'Данные успешно обновлены', reply_markup=config.menu())
    else:
        del config.arr[-1]
        bot.send_message(message.chat.id, 'Ваши последние изменения были удалены', reply_markup=config.menu())


@bot.message_handler(content_types=['text'])
def bot_list(message):
    if message.chat.type == 'private':
        if message.text == 'Список 🗒':
            if config.arr != []:
                print(config.arr)
                bot.send_message(message.chat.id, config.LIST(config.arr))
            else:
                bot.send_message(message.chat.id, 'Извините, но ваш список пуст')

        elif message.text == "Добавить 📌":
            add = bot.send_message(message.chat.id, 'Введите текст:')
            bot.register_next_step_handler(add, addF)

        elif message.text == "Нет, спасибо ❌":
            del config.arr[-1]
            bot.send_message(message.chat.id, 'Ваши последние изменения не были добавлены', reply_markup=config.menu())

        elif message.text == "Добавить ⏰":
            time = bot.send_message(message.chat.id, 'Введите время:')
            bot.register_next_step_handler(time, time_add)


bot.polling(none_stop=True)