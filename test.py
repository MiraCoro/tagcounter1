import datetime
from bs4 import BeautifulSoup
import requests
import logging
import pickle
import sqlite3
from tkinter import *
import re
import httplib2

current_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
base = "mybd.db"

# html_page = input("Please specify a site name: \n")
# html_page = requests.get(page)
def tagcounter(event):
    html_page = check_user_enter()
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
    #list = [x for x, y in dict.items()]

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
    if any(dict):
        Status['text'] = 'Success'
    else:
        Status['text'] ='Something went wrong'
    return list

def get_tage_from_base(event):
    if Enter_site.get():
        url = Enter_site.get()
        Enter_site.delete(0, END)
    else:
        url = List_of_sites.get(ACTIVE)
    import sqlite3
    import pickle
    conn = sqlite3.connect("mybd.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tags FROM Tags_of_sites WHERE url = ?",  (url,))
    tags = pickle.loads(cursor.fetchone()[0])
    conn.close()
    Tags['text'] = tags

def check_user_enter():
    if Enter_site.get():
        url = Enter_site.get()
        Enter_site.delete(0, END)
        #Check if url is correct
        if not re.match("http(s)*://.+", url):
            #If url correct (several literals with point between) and protocol doesn't specified - add protocol
            if re.search("\w+.\w{2,}", url):
                url = 'https://' + url
                h = httplib2.Http()
                resp = h.request(url, 'HEAD')
                if not any(resp):
                    Status['text'] = "Incorrect input: url is invalid. Try again"
                    Tags['text'] = ''

            #If url contains only one word, check is it synonym, was it correct written and it exists in synonyms list
            elif re.search("\w+", url):

                with open ('synonyms.yml', 'r') as doc:
                    doc.seek(0)
                    for string in doc.readlines():
                        if url in string:
                            url = re.search("https://.+", string).group(0)
                            break
                        else:
                            Tags['text'] = ''
                            Status['text'] = "Synonym's url not found. Try again"
            else:
                Tags['text'] = ''
                Status['text'] = "Incorrect input: url or synonym not found"

    else:
        Tags['text'] = ''
        url = List_of_sites.get(ACTIVE)
    return url



root = Tk()

frame = Frame(root)
scroll_sites = Scrollbar(frame, orient=VERTICAL)
List_of_sites = Listbox(frame, yscrollcommand=scroll_sites.set, selectbackground='black', selectforeground='red', selectmode=BROWSE)
scroll_sites.config(command=List_of_sites.yview)
scroll_sites.pack(side=RIGHT,fill=Y)
List_of_sites.pack(side=TOP, fill=BOTH, expand=1)
List_of_sites.bind('<Double-Button-1>', tagcounter)
List_of_sites.bind('<FocusOut>', lambda e: List_of_sites.selection_clear(0, END))
frame.pack()

with open('synonyms.yml', 'a+') as config:
    config.seek(0)
    for line in config.readlines():
        line = re.search("https://.+", line).group(0)
    #print (line.group(0))
        List_of_sites.insert(END, line)

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

Tags = Label(root, bg='black', fg='white')
Tags.config(wraplength=500, anchor=NW, justify=CENTER)
Tags.pack(fill=BOTH, expand=1, side=BOTTOM)

def add_to_syn(ss):
    line = Enter_site.get()
    url = re.search("http*://",line)
    synonym = re.search('^\w+', line)
    split = re.search(': ', line)
    if synonym and url and split:
        config.write(line)
        list_of_synonyms.insert(END, line)
    else:
        Status['text'] = "Incorrect input. Please specify synonym and url (e.g. google: https://google.com)"


list_of_synonyms = Listbox(root, selectbackground='yellow', selectforeground='green', selectmode=SINGLE)
list_of_synonyms.pack(side=BOTTOM)

with open('synonyms.yml', 'a+') as config:
    config.seek(0)
    for syn in config:
        line = config.readline()
        list_of_synonyms.insert(END, line)


Delete_button = Button(root, command=lambda list_of_synonyms=list_of_synonyms: list_of_synonyms.delete(ACTIVE), text="Delete a site from list")
Delete_button.pack(side=BOTTOM)

Add_button = Button(root, text="Add a site to synonyms's list")
Add_button.bind('<Button-1>', add_to_syn)
Add_button.pack(side=BOTTOM)

Enter_syn_site = Entry(root, width=20)
Enter_syn_site.pack(side=BOTTOM)

root.after(5000, tagcounter)
root.mainloop()

'''
Select_button = Button(root, text="Select a site", command=lambda: tagcounter(List_of_sites.get(ACTIVE)))
Select_button.pack()
list_of_synonyms = Listbox(root, selectbackground='blue', selectforeground='yellow', text="List of synonyms ", selectmode=SINGLE)



list_of_synonyms.pack(side=RIGHT, fill=BOTH, expand=1)

'''
