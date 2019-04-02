import sqlite3
conn = sqlite3.connect("mybd.db")
cursor = conn.cursor()
cursor.execute("SELECT tags FROM Tags_of_sites")
print(cursor.fetchall())