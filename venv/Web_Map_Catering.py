import folium
import pandas
from geopy.geocoders import ArcGIS

map = folium.Map(location=[51.41665, 21.96931], zoom_start=13.5, tiles='Stamen Terrain')

# MAKE POINT - Siedziba firmy
fg_siedziba = folium.FeatureGroup(name="Siedziba firmy")

iframe = folium.IFrame(html="Siedziba firmy", width=200, height=100)
fg_siedziba.add_child(folium.CircleMarker(location=[51.41665, 21.96931], radius = 4, popup=folium.Popup(iframe), fill_color = 'black', color = 'black', fill_opacity = 1))


# MAKE THREE FOLIUM CIRCULES - Darmowa dostawa
fg_darmowa = folium.FeatureGroup(name="Dostawy")

fg_darmowa.add_child(folium.Circle(location=[51.41665, 21.96931], popup='Dostawa 20zł ', fill_color='red', radius=3000, weight=2, color="gray", fill_opacity = 0.2))
fg_darmowa.add_child(folium.Circle(location=[51.41665, 21.96931], popup='Dostawa 10zł ', fill_color='orange', radius=2000, weight=2, color="gray", fill_opacity = 0.2))
fg_darmowa.add_child(folium.Circle(location=[51.41665, 21.96931], popup='Dostawa darmowa', fill_color='green', radius=1000, weight=2, color="gray", fill_opacity = 0.3))

# # ZAPYTANIE O ADRES DOSTAWY
#
# adres_dostawy = input("Adres dostawy: \nMiasto, ulica nr domu: ")
# nom = ArcGIS()
# adres = nom.geocode(adres_dostawy)
# lat_lon = adres[1]
# lat = adres[1][0]
# lon = adres[1][1]
#
# fg_adres_dostawy = folium.FeatureGroup(name="Adres dostawy")
# fg_adres_dostawy.add_child(folium.CircleMarker(location=[lat, lon], popup='Twój adres', fill_color='red', radius=4, weight=2, color="red", fill_opacity = 1))

# MAKE VISIBLE - All add.child()
map.add_child(fg_siedziba)
map.add_child(fg_darmowa)
# map.add_child(fg_adres_dostawy)
map.add_child(folium.LayerControl())

map.save("Map_Catering.html")

