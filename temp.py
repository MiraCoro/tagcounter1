import re
def get_tage_from_base():
    import sqlite3
    import pickle
    conn = sqlite3.connect("mybd.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tags FROM Tags_of_sites")
    #x = cursor.fetchall()
    #print (x)
    #for
    row = cursor.fetchall()
    print(row)
    for line in row:
        line = re.search("'('*')'", line).group(0)
        print(line)
        print(type(line))
        #row = cursor.fetchone()
    print(type(row))
    #x = {item: row[row.index(item)+1] for item in row if row.index(item) % 2 == 0}
    #print(x)
    #print(type(x))
    #z = pickle.loads(row)
    #print (z)
    #return z

a = 'https://mail.ru'
get_tage_from_base()