TOKEN = ''
import telebot

# Преветственный текст
hello_text = ["Привет, <b>{0.first_name}</b>.", "Во славу Первой Чувашской Империи", "Готов служить и повиноваться",
              "памагите, наса держать адин чувашаский психа в падавали и нэ выпускадъ наз пака мы ни напижем "
              "иму эта праграма", ]

# Стикеры
img = ['stic/AnimatedSticker.tgs', 'stic/AnimatedSticker1.tgs', 'stic/AnimatedSticker2.tgs',
       'stic/AnimatedSticker3.tgs', 'stic/AnimatedSticker4.tgs', 'stic/AnimatedSticker5.tgs',
       'stic/AnimatedSticker6.tgs', ]

arr = []


def menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    LIST = telebot.types.KeyboardButton("Список 🗒")
    ADD = telebot.types.KeyboardButton("Добавить 📌")
    DEL = telebot.types.KeyboardButton("Удалить 🗑")
    return (markup.add(LIST, ADD, DEL))


def LIST(arr):
    list_arr = ''
    for i in range(len(arr)):
        arr[i][0] = (str(i + 1) + ')')
        list_arr += str(arr[i][0]) + '   ' + str(arr[i][1]) + '    ' + str(arr[i][2]) + '\n'
    return (list_arr)