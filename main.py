import config
import telebot
import random

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    img = open(config.img[random.randint(0, len(config.img)) - 1], 'rb')
    bot.send_sticker(message.chat.id, img)
    bot.send_message(message.chat.id, config.hello_text[random.randint(0,
    len(config.hello_text) - 1)].format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=config.menu())


def add_f(message):
    add = message.text
    config.arr.append(['', add])
    print(config.arr)
    bot.send_message(message.chat.id, 'Текст успешно добавлен')
    time = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    time_add = telebot.types.KeyboardButton("Добавить ⏰")
    time_no = telebot.types.KeyboardButton("Нет, спасибо ❌")
    time.add(time_add, time_no)
    bot.send_message(message.chat.id, 'Хотите добавить время?'.format(message.from_user, bot.get_me()), reply_markup=time)


def data_add(message):
    data = message.text
    if data in ['1', '2', '3', '4', '5', '6', '7']:
        config.arr[len(config.arr) - 1].append('mod' + str(data))
        bot.send_message(message.chat.id, 'Дата изменена на {}'.format('mod' + str(data)), reply_markup=config.menu())
    else:
        try:
            data_boolean = False
            data = str(data)
            data = data.split('.')
            if 1 <= int(data[0]) <= 31:
                if 1 <= int(data[1]) <= 12:
                    data_boolean = True
            if data_boolean:
                data = '.'.join(data)
                config.arr[len(config.arr) - 1].append(data)
                bot.send_message(message.chat.id, 'Данные успешно обновлены ✅', reply_markup=config.menu())
                print(config.arr, 'test')
        except:
            if data == ['ОТМЕНА ❌']:  # Пока под вопросом
                config.arr[len(config.arr) - 1].append('mod1')  # Пока под вопросом
                bot.send_message(message.chat.id, 'Дата поставленна на каждый день', reply_markup=config.menu())
            else:
                bot.send_message(message.chat.id, 'Данные введены некоректно, попробуйте снова.', reply_markup=config.menu())
                data = bot.send_message(message.chat.id, 'Хотите указать дату?', reply_markup=config.cancel())
                bot.register_next_step_handler(data, data_add)


def time_add(message):
    time = message.text
    if time != "Нет, спасибо ❌":
        try:
            time_boolean = False
            time = str(time)
            time = time.split(':')
            if 0 <= int(time[0]) < 24:
                if 0 <= int(time[1]) < 60:
                    if 0 <= int(time[2]) < 60:
                        time_boolean = True
            if time_boolean:
                time = ':'.join(time)
                config.arr[len(config.arr) - 1].append(time)
                bot.send_message(message.chat.id, 'Данные успешно обновлены ✅')
                data = bot.send_message(message.chat.id, 'Хотите указать дату?', reply_markup=config.cancel())
                bot.register_next_step_handler(data, data_add)

            else:
                bot.send_message(message.chat.id, 'Вы ввели какую-то поебень 😱', reply_markup=config.menu())
                del config.arr[-1]
        except:
            bot.send_message(message.chat.id, 'Вы ввели какую-то поебень 😱', reply_markup=config.menu())
            del config.arr[-1]
    else:
        del config.arr[-1]
        bot.send_message(message.chat.id, 'Ваши последние изменения были удалены 🗑', reply_markup=config.menu())


#  Удаление
def del_index(message):
    bot.send_message(message.chat.id, config.LIST(config.arr))
    Del = message.text
    Del = Del.split(' ')
    arr_test = config.arr

    for i in range(len(Del) - 1):
        if int(Del[i]) < len(config.arr):
            del arr_test[int(Del[i]) - 1]
    config.arr = arr_test
    bot.send_message(message.chat.id, arr_test, reply_markup=config.menu())


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
            bot.register_next_step_handler(add, add_f)

        elif message.text == "Нет, спасибо ❌":
            del config.arr[-1]
            bot.send_message(message.chat.id, 'Ваши последние изменения не были добавлены 🗑', reply_markup=config.menu())

        elif message.text == "Добавить ⏰":
            time = bot.send_message(message.chat.id, 'Введите время:')
            bot.register_next_step_handler(time, time_add)

        elif message.text == "Удалить 🗑":
            bot.send_message(message.chat.id, config.LIST(config.arr))
            Del = bot.send_message(message.chat.id, 'Введите что вы хотите удалить:')
            bot.register_next_step_handler(Del, del_index)


bot.polling(none_stop=True)