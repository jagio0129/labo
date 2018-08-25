import folium

m = folium.Map(
  location=[35.681382,139.76608399999998],
  zoom_start=10
)

geo_json = "/home/vagrant/mount_folder/lab/data/geojson/syutoken.geojson"
topo_json = "/home/vagrant/mount_folder/lab/data/geojson/syutoken.topojson"

folium.GeoJson(
  geo_json,
  name="首都圏"
).add_to(m)

m.save('syutoken.html')
