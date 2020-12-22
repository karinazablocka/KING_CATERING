import sqlite3

conn = sqlite3.connect('catering.db')

cur = conn.cursor()
# cur.execute('''DROP table tabela_danie''')
cur.execute('''CREATE TABLE IF NOT EXISTS tabela_danie (id INTEGER, nazwa TEXT, cena FLOAT, dostepnosc INTEGER, kategoria TEXT)''')

dania = [(1, 'Kawa naturalna', 6, 1, 'napoj'),
         (2, 'Kawa inka', 5, 1, 'napoj'),
         (3, 'Herbata', 5.5, 1, 'napoj'),
         (4, 'Kakao z mlekiem', 5, 1, 'napoj'),
         (5, 'Kompot', 4, 1, 'napoj'),
         (6, 'Kefir', 4.5, 1, 'napoj'),
         
         (7, 'Barszcz z uszkami', 12.5, 1, 'zupa'),
         (8, 'Fasolowa', 13, 1, 'zupa'),
         (9, 'Jarzynowa', 9, 1, 'zupa'),
         (10, 'Kalafiorowa', 10, 1, 'zupa'),
         (11, 'Pomidorowa', 10, 1, 'zupa'),
         (12, 'Ogórkowa', 9, 1, 'zupa'),
         (13, 'Pieczarkowa', 11.5, 1, 'zupa'),
         (14, 'Rosół', 10, 1, 'zupa'),
         (15, 'Żurek', 12, 1, 'zupa'),
         
         (16, 'Bigos', 15, 1, 'potrawa'),
         (17, 'Gołąbki', 18, 1, 'potrawa'),
         (18, 'Karkówka w sosie', 22, 1, 'potrawa'),
         (19, 'Kotlet mielony', 20, 1, 'potrawa'),
         (20, 'Kotlet schabowy', 23, 1, 'potrawa'),
         (21, 'Kotlet de volaille', 23, 1, 'potrawa'),
         (22, 'Wątróbka wieprzowa w sosie', 18, 1, 'potrawa'),
         (23, 'Stek wołowy', 25, 1, 'potrawa'),
         (24, 'Zraz drobiowy', 19, 1, 'potrawa'),
         
         (25, 'Cukier', 2, 1, 'dodatek'),
         (26, 'Cytryna', 1, 1, 'dodatek'),
         (27, 'Bułka', 3, 1, 'dodatek'),
         (28, 'Ser żółty', 3, 1, 'dodatek'),
         (29, 'Ketchup', 2, 1, 'dodatek'),
         (30, 'Frytki', 6, 1, 'dodatek'),
         (31, 'Ziemniaki z wody', 5, 1, 'dodatek'),
         (32, 'Ryż', 4, 1, 'dodatek'),
         (33, 'Kasza gryczana', 4.5, 1, 'dodatek')]
        

cur.executemany('INSERT INTO tabela_danie VALUES (?,?,?,?,?)', dania)

records = cur.execute("SELECT * FROM tabela_danie")

for record in records:
    print(record)

conn.commit()
conn.close()