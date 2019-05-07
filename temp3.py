import re
def check_if_word(html_page):
    new = re.search("\w+", html_page).group(0)
    print(new)
    if html_page == new:
        print ('It\'s word')
    else:
        print('It\'s not word')


check_if_word('g&)')