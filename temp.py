def get_tage_from_base(url):
    import sqlite3
    import pickle
    conn = sqlite3.connect("mybd.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tags FROM Tags_of_sites WHERE url = ?",  (url,))
    print(pickle.loads(cursor.fetchone()[0]))
    conn.close()


a = 'https://mail.ru'
get_tage_from_base(a)

