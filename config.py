TOKEN = ''

import telebot

# Преветственный текст
hello_text = ["Привет, <b>{0.first_name}</b>.", "Во славу Первой Чувашской Империи", "Готов служить и повиноваться",
              "памагите, наса держать адин чувашаский психа в падавали и нэ выпускадъ наз пака мы ни напижем "
              "иму эта праграма", ]

# Стикеры
img = ['img/AnimatedSticker.tgs', 'img/AnimatedSticker1.tgs', 'img/AnimatedSticker2.tgs',
       'img/AnimatedSticker3.tgs', 'img/AnimatedSticker4.tgs', 'img/AnimatedSticker5.tgs',
       'img/AnimatedSticker6.tgs', ]

arr = []


########################################################################################################################

sql = open('text/main.txt', 'r', encoding="utf-8").read().split('\n')
sql = sql[:-1]
a = [[]]
b = []
x, y = 1, 5
for i in sql:
    a += str(i).split('   ')
for i in range(len(a) // 4):
    b.append([])
    b[i] += a[x:y]
    x += 4
    y += 4
arr = b


def menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    LIST = telebot.types.KeyboardButton("Список 🗒")
    ADD = telebot.types.KeyboardButton("Добавить 📌")
    DEL = telebot.types.KeyboardButton("Удалить 🗑")
    return (markup.add(LIST, ADD, DEL))


def cancel():
    cancel_ = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    end = telebot.types.KeyboardButton("ОТМЕНА ❌")
    return cancel_.add(end)


def accept():
    accept_ = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    no = telebot.types.KeyboardButton("ОТМЕНА ❌")
    yes = telebot.types.KeyboardButton("ПРИНЯТЬ ✅")
    return accept_.add(no, yes)


def LIST(arr):
    list_arr = ''
    for i in range(len(arr)):
        arr[i][0] = (str(i + 1) + ')')
        list_arr += str(arr[i][0]) + '   ' + str(arr[i][1]) + '   ' + str(arr[i][2]) + '   ' + str(arr[i][3]) + '\n'
    return (list_arr)


def update():
    sql = open('text/main.txt', 'w', encoding="utf-8")
    sql.write(LIST(arr))
    sql.close()
