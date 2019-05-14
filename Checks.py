import httplib2
import re
def check_user_enter(x):
    if not re.match("https://.+|https://.+", x):
         #If url correct (several literals with point between) and protocol doesn't specified - add protocol
        if re.search("\w+.\w{2,}", x):
            url = 'https://' + x
            h = httplib2.Http()
            resp = h.request(url, 'HEAD')
            if not any(resp):
                print("Incorrect input: url is invalid. Try again")
            else:
                print("Url + https")


            #If url contains only one word, check is it synonym, was it correct written and it exists in synonyms list
        elif re.search("\w+", x):
            with open ('synonyms.yml', 'r') as doc:
                doc.seek(0)
                for string in doc.readlines():
                    if x in string:
                        url = re.search("https://.+", string).group(0)
                        print("Synonym found")
                        break
                    else:
                        print("Synonym's url not found. Try again")
        else:
            print("Not a site")
    else:
        url = x
        print("Url is valid")

    return url

#y = 'https://effbot.org/'
y='yandx.ru'

check_user_enter(y)