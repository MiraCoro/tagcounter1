import re
with open('synonyms.yml', 'a+') as config:
    config.seek(0)
    for line in config.readlines():

        line = (re.search("https://.+", line)).group(0)
        #line = config.readline()
        print(line)