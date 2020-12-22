import sqlite3

conn = sqlite3.connect('catering.db')

cur = conn.cursor()
cur.execute('''DROP table menu''')

# dania = [(1, 'schabowy', 23.5),
#         (2, 'spagetti', 15),
#         (3, 'ogórkowa', 8)]
#
# cur.executemany('INSERT INTO menu VALUES (?,?,?)', dania)

records = cur.execute("SELECT * FROM menu")

for record in records:
    print(record)

conn.commit()
conn.close()