### IMPORT BIBLIOTEK

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

import folium
import pandas
from geopy.geocoders import ArcGIS

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///catering.db'
db=SQLAlchemy(app)


### TWORZENIE TABEL W BAZIE DANYCH catering.db (tabela tabela_danie z daniami i cenami utworzona oddzialenie "menu_creating_db.py")

##  TABELA "tabela_klient" Z DANYMI klienta Z Formularza Zamówienia ZE STRONY /Zamowienie/

class Data_klient(db.Model):
    __tablename__="tabela_klient"
    id_zamowienie = db.Column('Id', db.Integer(), primary_key=True)
    name_klient = db.Column('Imie i nazwisko', db.String(255), nullable=False)
    tel_klient = db.Column('Telefon', db.Integer())
    email_klient = db.Column('Email', db.String(255), nullable=False, unique=True)

    def __init__(self, name_klient, tel_klient, email_klient  ):
        self.name_klient=name_klient
        self.tel_klient=tel_klient
        self.email_klient=email_klient

##  TABELA "data" Z DANYMI Z Formularza Kontaktowego ZE STRONY /Kontakt/

class Data(db.Model):
    __tablename__="data"
    id = db.Column('Id', db.Integer(), primary_key=True)
    imie_ = db.Column('Imie i nazwisko', db.String(255), nullable=False)
    email_ = db.Column('Email', db.String(255), nullable=False)
    telefon_ = db.Column('Telefon', db.Integer())
    wiadomosc_ = db.Column('Wiadomosc', db.String(500), nullable=False)

    def __init__(self, imie_, email_, telefon_, wiadomosc_):
        self.imie_=imie_
        self.email_=email_
        self.telefon_=telefon_
        self.wiadomosc_=wiadomosc_


##  TABELA "zamowienie" Z DANYMI adresowymi Z Formularza Zamówienia ZE STRONY /Zamowienie/

class Data_zamowienie(db.Model):
    __tablename__="zamowienie"
    id_zamowienie = db.Column('Id', db.Integer(), primary_key=True)
    miasto_zamowienie = db.Column('Miasto', db.String(255), nullable=False)
    kod_zamowienie = db.Column('Kod pocztowy', db.String(255), nullable=False)
    ulica_zamowienie = db.Column('Ulica', db.String(255), nullable=False)
    nr_budynku_zamowienie = db.Column('Nr budynku', db.Integer())
    nr_mieszkania_zamowienie = db.Column('Nr mieszkania', db.Integer())
    name_zamowienie = db.Column('Imie i nazwisko', db.String(255), nullable=False)
    tel_zamowienie = db.Column('Telefon', db.Integer())
    email_zamowienie = db.Column('Email', db.String(255), nullable=False)

    def __init__(self, miasto_zamowienie, kod_zamowienie, ulica_zamowienie, nr_budynku_zamowienie, 
                 nr_mieszkania_zamowienie, name_zamowienie, tel_zamowienie, email_zamowienie  ):
        self.miasto_zamowienie=miasto_zamowienie
        self.kod_zamowienie=kod_zamowienie
        self.ulica_zamowienie=ulica_zamowienie
        self.nr_budynku_zamowienie=nr_budynku_zamowienie
        self.nr_mieszkania_zamowienie=nr_mieszkania_zamowienie
        self.name_zamowienie=name_zamowienie
        self.tel_zamowienie=tel_zamowienie
        self.email_zamowienie=email_zamowienie


##  TABELA "zamowienie_danie" Z DANYMI Z Formularza Zamówienia ZE STRONY /Zamowienie/ z zamówionymi daniami

class Data_zamowienie_danie(db.Model):
    __tablename__="zamowienie_danie"
    id = db.Column('Id', db.Integer(), primary_key=True)
    id_zamowienie = db.Column('Id_zamowienia', db.Integer(), nullable=False)
    id_menu = db.Column('Id_menu', db.Integer(), nullable=False)
    liczba_sztuk = db.Column('liczba_sztuk', db.Integer(), nullable=False)

    def __init__(self, id_zamowienie, id_menu, liczba_sztuk):
        self.id_zamowienie=id_zamowienie
        self.id_menu=id_menu
        self.liczba_sztuk=liczba_sztuk


### CO ZAWIERA SIĘ NA POSZCZEGÓLNYCH STRONACH

##  STRONA home.html - Home
@app.route('/')
def home():
    return render_template("home.html")

##  STRONA Map_Catering.html - Mapa dostaw
@app.route('/Map_Catering/')
def Map_Catering():
    return render_template("Map_Catering.html")

##  STRONA Mappp_Catering.html - Co dzieje się po naciśnięciu przycisku na Map_Catering.html - Mapa dostaw
@app.route('/Dziekuje_mapa', methods=['GET', 'POST'])
def Dziekuje_mapa():
    if request.method == 'POST':
        adres_dostawy = request.form["map_adres"]
        print(adres_dostawy)


        map = folium.Map(location=[51.41665, 21.96931], zoom_start=13, tiles='Stamen Terrain')

        # MAKE POINT - Siedziba firmy
        fg_siedziba = folium.FeatureGroup(name="Siedziba firmy")

        iframe = folium.IFrame(html="Siedziba firmy", width=200, height=100)
        fg_siedziba.add_child(
            folium.CircleMarker(location=[51.41665, 21.96931], radius=4, popup=folium.Popup(iframe), fill_color='black',
                                color='black', fill_opacity=1))

        # MAKE THREE FOLIUM CIRCULES - Darmowa dostawa
        fg_darmowa = folium.FeatureGroup(name="Dostawy")

        fg_darmowa.add_child(
            folium.Circle(location=[51.41665, 21.96931], popup='Dostawa 20zł ', fill_color='red', radius=3000, weight=2,
                          color="gray", fill_opacity=0.2))
        fg_darmowa.add_child(
            folium.Circle(location=[51.41665, 21.96931], popup='Dostawa 10zł ', fill_color='orange', radius=2000,
                          weight=2, color="gray", fill_opacity=0.2))
        fg_darmowa.add_child(
            folium.Circle(location=[51.41665, 21.96931], popup='Dostawa darmowa', fill_color='green', radius=1000,
                          weight=2, color="gray", fill_opacity=0.3))

        # ZAPYTANIE O ADRES DOSTAWY

        nom = ArcGIS()
        adres = nom.geocode(adres_dostawy)
        lat_lon = adres[1]
        lat = adres[1][0]
        lon = adres[1][1]

        fg_adres_dostawy = folium.FeatureGroup(name="Adres dostawy")
        fg_adres_dostawy.add_child(
            folium.CircleMarker(location=[lat, lon], popup='Twój adres', fill_color='red', radius=4, weight=2,
                                color="red", fill_opacity=1))

        # MAKE VISIBLE - All add.child()
        map.add_child(fg_siedziba)
        map.add_child(fg_darmowa)
        map.add_child(fg_adres_dostawy)
        map.add_child(folium.LayerControl())

        map.save("templates/Mappp_Catering.html")

        html_str = """
<!DOCTYPE html>
<head>
    <link href="../static/main.css" rel="stylesheet">
</head>
    <body>
        <div class="container">
            <strong><nav>
                    <ul class="menu">
                        <li><a href="{{ url_for('home') }}">Home</a></li>
                        <li><a href="{{ url_for('Zamowienie') }}">Zamowienie</a></li>
                        <li><a href="{{ url_for('Map_Catering') }}">Mapa dostaw</a></li>
                        <li><a href="{{ url_for('Kontakt') }}">Kontakt</a></li>
                    </ul>
            </nav></strong>
        </div>
    </body>"""

        with open('templates/Mappp_Catering.html') as f:
            updatedfile = html_str + '\n' + f.read()
        with open('templates/Mappp_Catering.html', 'w') as f:
            f.write(updatedfile)

    return render_template("Mappp_Catering.html")


##  STRONA Kontakt.html - Kontakt
@app.route('/Kontakt/')
def Kontakt():
    return render_template("Kontakt.html")

##  STRONA Zamowienie.html - Zamówienie
@app.route('/Zamowienie/')
def Zamowienie():
    con = sqlite3.connect("catering.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from tabela_danie where kategoria='zupa'")
    zupy = cur.fetchall();
    cur.execute("select * from tabela_danie where kategoria='napoj'")
    napoje = cur.fetchall();
    cur.execute("select * from tabela_danie where kategoria='potrawa'")
    potrawy = cur.fetchall();
    cur.execute("select * from tabela_danie where kategoria='dodatek'")
    dodatki = cur.fetchall();
    return render_template("Zamowienie.html", zupy = zupy, napoje=napoje, potrawy=potrawy, dodatki=dodatki)

##  STRONA Dziekuje_za_wiadomosc.html - Co dzieje się po naciśnięciu przycisku na Kontakt.html
@app.route('/Dziekuje_za_wiadomosc', methods=['POST'])
def Dziekuje_za_wiadomosc():
    if request.method == 'POST':
        name = request.form["name_name"]
        email = request.form["email_name"]
        tel = request.form["tel_name"]
        wiadomosc = request.form["wiadomosc_name"]
        print(name, email, tel, wiadomosc)
        data=Data(name, email, tel, wiadomosc)
        db.session.add(data)
        db.session.commit()
        return render_template("Dziekuje_za_wiadomosc.html")

##  STRONA Dziekuje_za_zamowienie.html - Co dzieje się po naciśnięciu przycisku na Zamowienie.html
@app.route('/Dziekuje_za_zamowienie', methods=['POST'])
def Dziekuje_za_zamowienie():
#   ZBIERANIE DANYCH ADRESOWYCH I ZAPISANIE ICH DO TABELI "zamówienie"
    if request.method == 'POST':
        miasto_zamowienie = request.form["miasto_zamowienie"]
        kod_zamowienie = request.form["kod_zamowienie"]
        ulica_zamowienie = request.form["ulica_zamowienie"]
        nr_budynku_zamowienie = request.form["nr_budynku_zamowienie"]
        nr_mieszkania_zamowienie = request.form["nr_mieszkania_zamowienie"]
        name_zamowienie = request.form["name_zamowienie"]
        tel_zamowienie = request.form["tel_zamowienie"]
        email_zamowienie = request.form["email_zamowienie"]

        zamowienie = Data_zamowienie(miasto_zamowienie, kod_zamowienie, ulica_zamowienie,
                               nr_budynku_zamowienie, nr_mieszkania_zamowienie, name_zamowienie,
                               tel_zamowienie, email_zamowienie)
        db.session.add(zamowienie)
        db.session.commit()

#   ZBIERANIE DANYCH Z ZAMÓWIONYMI DANIAMI I ZAPISANIE ICH DO TABELI "zamowienie_danie"
#   ZAPISANIE KTÓRE DANIA (CHECKBOXES) ZOSTAŁY ZAZNACZONE
    if request.method == 'POST':
        dania = (request.form.getlist('dania'))
    print(dania)

#   ZAPISANIE ILE SZTUK DAŃ PRZY ZAZNACZONYCH CHECKBOXES ZOSTAŁO ZAMÓWIONE
    b=[]
    for danie in dania:
        for key, val in request.form.items():
            print(key)
            print("DANIA:")
            print(dania)
            print("KEY:")
            print(key)
            if (key == ("liczba_sztuk"+danie)) and val != "":
                b.append((danie, val))

#   WYDOBYCIE Z TABELI "zamowienie" OSTATNIEGO ID ABY PRZYPORZĄDKOWAĆ DANIA I ICH LICZBĘ DO KONKRETNEGO ZAMÓWIENIA
        con = sqlite3.connect("catering.db")
        cur = con.cursor()
        con.row_factory = sqlite3.Row
        cur.execute("SELECT Id FROM zamowienie ORDER BY Id DESC LIMIT 1")
        id_zamowienie = cur.fetchall();
        con.commit()

#   ZAPISANIE DANYCH Z ZAMÓWIONYMI DANYMI I ID ZAMOWIENIA W TABELI "dania_zamowienie"
    for i in b:
        dania_zamowienie = Data_zamowienie_danie(id_zamowienie[0][0], i[0], i[1])
        db.session.add(dania_zamowienie)

    db.session.commit()

#   ZWRÓCENIE STRONY Z INFORMACJĄ, ŻE ZAMÓWIENIE ZOSTAŁO ZŁOŻONE
    return render_template("Dziekuje_za_zamowienie.html")

db.create_all()

if __name__=='__main__':
    app.debug=True              ### Gdy jest TRUE wyskakują błędy na stronie (Na koniec chcemy mieć tu FALSE aby uzytkownicy nie widzieli błędów)
    app.run()
