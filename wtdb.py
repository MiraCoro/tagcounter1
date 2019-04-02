import pickle
import sqlite3



def write_to_db(dct, bd):
    from main import site_name, html_page, current_date
    bdict = pickle.dumps(dct)

    conn = sqlite3.connect(bd)
    cursor = conn.cursor()


    cursor.execute('''CREATE TABLE IF NOT EXISTS Tags_of_sites
                  (site_name text, url text, date text, tags blob)''')

    cursor.execute('''INSERT INTO Tags_of_sites VALUES (?, ?, ?, ?)''', (site_name, html_page, current_date, bdict))

#cursor.execute('INSERT INTO Tag_of_sites VALUES (?, ?)', (id, pickle.dumps(dict)))
    conn.commit()
    conn.close()
    return bd
