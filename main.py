import config
import telebot
import random

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    img = open(config.img[random.randint(0, len(config.img)) - 1], 'rb')
    bot.send_sticker(message.chat.id, img)
    bot.send_message(message.chat.id, config.hello_text[random.randint(0,
                                                                       len(config.hello_text) - 1)].format(
        message.from_user, bot.get_me()), parse_mode='html', reply_markup=config.menu())


def add_f(message):
    add = message.text
    config.arr.append(['', add])
    print(config.arr)
    bot.send_message(message.chat.id, 'Текст успешно добавлен')
    time = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    time_add = telebot.types.KeyboardButton("Добавить ⏰")
    time_no = telebot.types.KeyboardButton("Нет, спасибо ❌")
    time.add(time_add, time_no)
    bot.send_message(message.chat.id, 'Хотите добавить время?'.format(message.from_user, bot.get_me()),
                     reply_markup=time)


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
            else:
                bot.send_message(message.chat.id, 'Данные введены некоректно, попробуйте снова.',
                                 reply_markup=config.menu())
                data = bot.send_message(message.chat.id, 'Хотите указать дату?', reply_markup=config.cancel())
                bot.register_next_step_handler(data, data_add)
        except:
            if data == ['ОТМЕНА ❌']:  # Пока под вопросом
                config.arr[len(config.arr) - 1].append('mod1')  # Пока под вопросом
                bot.send_message(message.chat.id, 'Дата поставленна на каждый день', reply_markup=config.menu())
            else:
                bot.send_message(message.chat.id, 'Данные введены некоректно, попробуйте снова.',
                                 reply_markup=config.menu())
                data = bot.send_message(message.chat.id, 'Хотите указать дату?', reply_markup=config.cancel())
                bot.register_next_step_handler(data, data_add)

    config.update()


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


def del_index(message):
    del_input = message.text
    arr_test = config.arr * 2
    arr_test = arr_test[: int(len(arr_test) / 2)]  # Костыль, не трогать
    try:
        del arr_test[(int(del_input)) - 1]
    except:

        del_input = del_input.split(' ')

        for i in range(len(del_input)):
            try:
                del_input[i] = int(del_input[i])
            except:
                continue

        del_input = reversed(sorted(del_input))
        print(del_input)

        for i in del_input:
            print(i)
            try:
                del arr_test[int(i) - 1]
            except:
                continue

    if arr_test != []:
        bot.send_message(message.chat.id, config.LIST(arr_test))
    else:
        bot.send_message(message.chat.id, 'Ваш список окажется пустым')
    del_accept = bot.send_message(message.chat.id, 'Хототе ли вы внести изменения?', reply_markup=config.accept())

    def del_end(message):
        del_accept = message.text
        if del_accept == 'ПРИНЯТЬ ✅':
            config.arr = arr_test
            config.update()
            bot.send_message(message.chat.id, 'Массив изменён', reply_markup=config.menu())
        else:
            bot.send_message(message.chat.id, 'Изменения не были добавлены', reply_markup=config.menu())

    bot.register_next_step_handler(del_accept, del_end)


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
            bot.send_message(message.chat.id, 'Ваши последние изменения не были добавлены 🗑',
                             reply_markup=config.menu())

        elif message.text == "Добавить ⏰":
            time = bot.send_message(message.chat.id, 'Введите время:')
            bot.register_next_step_handler(time, time_add)

        elif message.text == "Удалить 🗑":
            bot.send_message(message.chat.id, config.LIST(config.arr))
            del_input = bot.send_message(message.chat.id, 'Введите что вы хотите удалить:')
            bot.register_next_step_handler(del_input, del_index)

        else:
            bot.send_message(message.chat.id, 'Простите, я не понимаю')


bot.polling(none_stop=True)
