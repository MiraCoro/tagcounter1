import datetime
from bs4 import BeautifulSoup
import requests
from collections import Counter
import re
#html_page = 'https://google.com'
html_page = input("Please specify a site name: \n")
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


site_name = (soup.find('title')).contents[0]
print (site_name)

current_date = (datetime.datetime.now()).strftime("%Y-%m-%d")
print(current_date)