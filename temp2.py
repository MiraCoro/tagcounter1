import re
import re
def test_syn(html_page):

    if html_page == re.search("\w+", html_page).group(0):
        with open ('synonyms.yml', 'r') as doc:
            doc.seek(0)
            for string in doc.readlines():
                if html_page in string:
                    html_page = re.search("https://.+", string).group(0)
                    print(html_page)
                    break
                else:
                    print('AA')

    else:
        print('Not a word')
    return html_page


test_syn('goole')

