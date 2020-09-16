import pyttsx3
import time
import config
import datetime


engine = pyttsx3.init()
print(config.arr)
while True:
    time.sleep(1)

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

    print(time.ctime().split(' ')[3])
    for i in arr:
        if i[2] == time.ctime().split(' ')[3]:
            if i[3] == (datetime.datetime.today().strftime("%d.%m.%Y")) or i[3] == 'mod1':
                engine.say(i[1])
                engine.runAndWait()
