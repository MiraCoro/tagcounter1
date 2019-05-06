import datetime
from bs4 import BeautifulSoup
import requests
import logging
import pickle
import sqlite3
from tkinter import *
import re
#from temp import get_tage_from_base

current_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
base = "mybd.db"

# html_page = input("Please specify a site name: \n")
# html_page = requests.get(page)
def tagcounter(event):
    if List_of_sites.get(ACTIVE) and not Enter_site.get():
        html_page = List_of_sites.get(ACTIVE)
    else:
        html_page = Enter_site.get()
    #html_page = Enter_site.get()
    #print(html_page)
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

    Tags['text'] = dict
    list = [x for x, y in dict.items()]

    bdict = pickle.dumps(dict)
    site_name = (soup.find('title')).contents[0]

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
    if dict:
        Status['text'] = 'Success'
    else:
        Status['text'] ='Somthing went wrong'
    return list

def get_tage_from_base(event):
    url = html_page = List_of_sites.get(ACTIVE)
    import sqlite3
    import pickle
    conn = sqlite3.connect("mybd.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tags FROM Tags_of_sites WHERE url = ?",  (url,))
    tags = pickle.loads(cursor.fetchone()[0])
    conn.close()
    Tags['text'] = tags

root = Tk()


List_of_sites = Listbox(root, selectbackground='black', selectforeground='red', selectmode=SINGLE)
List_of_sites.pack(side=TOP, fill=BOTH, expand=1)

with open('synonyms.yml', 'r') as config:
    for line in config.readlines():
        line = re.search("https://.+", line).group(0)
    #print (line.group(0))
        List_of_sites.insert(END, line)
Select_button = Button(root, text="Select a site", command=lambda: tagcounter)
Select_button.pack(side=TOP)

Enter_site = Entry(root, width=20)
Enter_site.pack(side=TOP)

Get_tags_button = Button(root, text="Get tags")

Get_tags_button.bind('<Button-1>', tagcounter)
Get_tags_button.pack(side=TOP)


Show_from_db_button = Button(root, text="Show tags from database") #запрос и раскодирование
Show_from_db_button.bind('<Button-1>', get_tage_from_base)
Show_from_db_button.pack(side=TOP)

Status = Label(root, bg='white', fg='green', width=60)
Status.pack(side=BOTTOM)

Tags = Label(root, bg='black', fg='white', width=60)
Tags.pack(expand=1, fill=BOTH, side=BOTTOM)
syn_sites = open ('synonyms.yml', 'a')

Delete_button = Button(root, command=lambda syn_sites=syn_sites: syn_sites.delete(ACTIVE), text="Delete a site from list")
Delete_button.pack(side=BOTTOM)

Add_button = Button(root, text="Add a site to synonyms's list")
Add_button.bind('<Button-1>', lambda syn_sites=syn_sites: syn_sites.write(Enter_site.get()))
Add_button.pack(side=BOTTOM)

#lambda List_of_sites=List_of_sites: List_of_sites.delete(ACTIVE)
Enter_syn_site = Entry(root, width=20)
Enter_syn_site.pack(side=BOTTOM)

list_of_synonyms = Listbox(root, selectbackground='yellow', selectforeground='green', selectmode=SINGLE)
list_of_synonyms.pack(side=BOTTOM)
with open ('synonyms.yml', 'r') as syn_sites:
    for line in syn_sites.readlines():
        list_of_synonyms.insert(END, line)




root.after(5000, tagcounter)
root.mainloop()

'''
Select_button = Button(root, text="Select a site", command=lambda: tagcounter(List_of_sites.get(ACTIVE)))
Select_button.pack()
list_of_synonyms = Listbox(root, selectbackground='blue', selectforeground='yellow', text="List of synonyms ", selectmode=SINGLE)

for syn in config:
    line = config.readline()
    list_of_synonyms.insert(END, line)

list_of_synonyms.pack(side=RIGHT, fill=BOTH, expand=1)

'''
syn_sites.close()