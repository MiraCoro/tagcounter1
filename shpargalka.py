import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
conn.commit()
conn.close()


# Программирование GUI
# https://docs.python.org/3/library/tkinter.html
from tkinter import *
from tkinter.messagebox import showinfo
def reply():
    showinfo(title='popup', message='Button pressed!')
window = Tk()
button = Button(window, text='press', command=reply)
button.pack()
window.mainloop()

# Параметры командной строки
import sys
sys.argv

# argparse
# https://docs.python.org/3/library/argparse.html
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

args = parser.parse_args()


 Логирование
# logging
# https://docs.python.org/3/library/logging.html
import logging
# настройка корневого логгера
# отправка сообщений stderr
logging.basicConfig(level=logging.DEBUG)
# отправка сообщений в stdout
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# отправка сообщений в файл
logging.basicConfig(filename="info.log", level=logging.DEBUG)
logging.warning("My message")

# Создание пользовательского логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info('I told you info')
logger.error('I told you error')

# Более гибкая настройка логгера с помощью handler и formatter
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

logger.parent
logger.name

# Пример имени "foo.bar.my_module"
# логгеры создают иерархию соответсвующую имени модуля
# Иерархия начинается с с логера 'root'.
# Если для логера не определены настройки, они берутся из
# родительского логера
