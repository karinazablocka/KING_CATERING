import sqlite3

conn = sqlite3.connect('catering.db')

cur = conn.cursor()
cur.execute('''DROP table zamowienie''')

records = cur.execute("SELECT * FROM zamowienie")

for record in records:
    print(record)

conn.commit()
conn.close()