import datetime
from bs4 import BeautifulSoup
import requests
import logging
import pickle
import sqlite3
current_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
print(current_date)
base = "mybd.db"

def tagcounter(html_page):
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
    #print(dict)
    list = [x for x, y in dict.items()]

    bdict = pickle.dumps(dict)
    '''
    print(bdict)
    print(type(bdict))
    z = pickle.loads(bdict)
    print(z)
    print(type(z))
'''
    print(html_page)
    site_name = (soup.find('title')).contents[0]
    #print(site_name)

    conn = sqlite3.connect(base)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Tags_of_sites
                  (site_name text, url text, date text, tags blob)''')

    cursor.execute('''INSERT INTO Tags_of_sites VALUES (?, ?, ?, ?)''', (site_name, html_page, current_date, bdict))

    conn.commit()
    conn.close()

    logger = logging.getLogger("tagcounter")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler("tagcounter.log")

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)

    logger.info(site_name)
    return list

x = 'https://python-scripts.com/'
tagcounter(x)