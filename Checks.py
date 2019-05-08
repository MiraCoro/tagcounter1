import httplib2
import re
#h = httplib2.Http()
#resp = h.request("http://www.google.com", 'HEAD')
#print(resp)

def check_user_enter(url):
    h = httplib2.Http()
   #Check if url is correct
    if not re.match("http(s)*://.+", url):
        # If url correct (several literals with point between) and protocol doesn't specified - add protocol
        if re.search("\b\w+\.\w{2,}", url):
            url = 'https://' + url
            #If url contains only one word, check is it synonym, was it correct written and it exists in synonyms list
        elif re.search("\b\w+", url):

            with open ('synonyms.yml', 'r') as doc:
                doc.seek(0)
                for string in doc.readlines():
                    if url in string:
                        url = re.search("https://.+", string).group(0)
                        break
                    else:
                    print("Synonym's url not found. Try again")
            else:
                Tags['text'] = ''
                Status['text'] = "Incorrect input: url or synonym not found"

    else:
        if any(resp):
            print(url)
        else:
            print("Url not found")
    return url