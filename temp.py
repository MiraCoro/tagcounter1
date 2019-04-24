def get_tage_from_base():
    from bs4 import BeautifulSoup
    import sqlite3
    import pickle
    import requests
    #soup = BeautifulSoup(requests.get(html_page).content, 'html.parser')
    #tags = soup.find_all()
    #site_name = (soup.find('title')).contents[0]
    #print(html_page)
    conn = sqlite3.connect("mybd.db")
    cursor = conn.cursor()
    #cursor.execute("SELECT tags FROM Tags_of_sites WHERE url='https://mail.ru'")
    cursor.execute("SELECT url FROM Tags_of_sites")
    x = cursor.fetchone()
    print(''.join(x))
    print(type(x))
    '''
    #row2 = cursor.fetchone()
    #row2 = cursor.fetchall()
    #print(row2)
    # print(type(row2))
    for line in row2:
        print(line)
        #print(type(line))
        #row2 = cursor.fetchone()
        '''
    #row2 = cursor.fetchone()
    #while row2 is not None:
     #   print(cursor.fetchone())


    conn.close()



a = 'https://python-scripts.com/'
get_tage_from_base()

'''


    
'''