import pyttsx3
import time
import config


engine = pyttsx3.init()

while True:
    for i in config.arr:
        print((time.ctime()).split(' ')[4])
        if i[2][1:] == time.ctime().split(' ')[4]:
            engine.say(i[1])
            engine.runAndWait()