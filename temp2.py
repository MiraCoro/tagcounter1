import re
with open('synonyms.yml', 'r') as config:
    for line in config.readlines():
        line = (re.search("https://.+", line)).group(0)
        #line = config.readline()
        print(line)