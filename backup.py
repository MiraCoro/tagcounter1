import datetime
from bs4 import BeautifulSoup
import requests
import logging
import wtdb
import pickle
import sqlite3
import tkinter

html_page = input("Please specify a site name: \n")

#print(page)
#html_page = requests.get(page)
tag_count = 0
dict = {}
soup = BeautifulSoup(requests.get(html_page).content, 'html.parser')
tags = soup.find_all()

ts = [tag.name for tag in tags]
for tag in ts:
    if tag:
        tag_count += 1
        dict.update({tag: tag_count})
    else:
        dict[tag] = tag_count
print(dict)


site_name = (soup.find('title'))
site_name = site_name.contents[0]
print (site_name)

current_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
print(current_date)

logger = logging.getLogger("tagcounter")
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler("tagcounter.log")

formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

logger.info(site_name)
base = "mybd.db"

bdict = pickle.dumps(dict)




#def write_to_db(bd):

conn = sqlite3.connect(base)
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS Tags_of_sites
                  (site_name text, url text, date text, tags blob)''')

cursor.execute('''INSERT INTO Tags_of_sites VALUES (?, ?, ?, ?)''', (site_name, html_page, current_date, bdict))

#cursor.execute('INSERT INTO Tag_of_sites VALUES (?, ?)', (id, pickle.dumps(dict)))
conn.commit()
conn.close()


#wtdb.write_to_db(base)