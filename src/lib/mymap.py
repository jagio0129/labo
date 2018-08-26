import folium
import geocoder
import json
import pandas as pd

# 緯度経度から市区町村名を取得
def get_city_form_geocoder(latitude, longitude):
  g = geocoder.google([latitude, longitude],method='reverse',language="ja")
  return g.city

# 市区町村名からgeojson_recordを取得
def get_record_form_city(json_path, city):
  j = geojson_parser(json_path)
  for v in j["features"]:
    if v["properties"]["N03_004"] == city:
      jprint(v)
      break

# geojsonをパース
def geojson_parser(json_path):
  f = open(json_path,'r')
  return json.load(f)

# geojsonを反映したmapをhtmlで保存
def gen_geojson_map(geojson_path):
  # folium init
  m = folium.Map(
    location=[35.681382,139.76608399999998],
    zoom_start=10
  )

  # add geojson
  folium.GeoJson(
    geojson_path,
    name="首都圏"
  ).add_to(m)

  m.save('syutoken.html')

# jsonを整形して表示
def jprint(data):
  print(json.dumps(data, indent=2))

# 市区町村ごとのユーザ数をカウント
def counter(data_path):
  df = pd.read_csv(data_path)
  print(df)