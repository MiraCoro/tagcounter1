import re

config = open('synonyms.yml', 'r')

for site in config:
    #print(type(site))
    exp = 'https://.+'
    line = re.search('https://.+', site)
    print (line.group(0))

config.close()
