import sqlite3

conn = sqlite3.connect('catering.db')

cur = conn.cursor()
cur.execute('''DELETE FROM data''')

records = cur.execute("SELECT * FROM data")

for record in records:
    print(record)

conn.commit()
conn.close()