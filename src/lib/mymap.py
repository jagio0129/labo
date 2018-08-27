import folium
import geocoder
import json
import pandas as pd
import os
import time
import branca

# 緯度経度から市区町村名を取得
def get_city_form_geocoder(latitude, longitude, cnt):
  g = geocoder.google([latitude, longitude],method='reverse',language="ja")
  if not g.city == None:
    return g.city
  cnt += 1
  if cnt == 10:
    return None
  return get_city_form_geocoder(latitude, longitude, cnt)

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

def city_list(json_path):
  j = geojson_parser(json_path)

# geojsonを反映したmapをhtmlで保存
def gen_geojson_map(geojson_path, save_path):
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

  m.save(os.path.join(save_path, 'syutoken.html'))
  print("Create html file")

def mygen_geojson_map(geojson_path, number_of_city, save_path):
  print("Create html file")
  noc_df = pd.read_csv(number_of_city, na_values=[' '])

  
  colorscale = branca.colormap.linear.PuRd_09.scale(0, 10)
  employed_series = noc_df.set_index('city')['number']

  def style_function(feature):
    employed = employed_series.get(str(feature['properties']['N03_004']), None)
    return {
      'fillOpacity': 0.7,
      'weight': 0,
      'fillColor': '#yellow' if employed is None else colorscale(employed)
    }

  # folium init
  m = folium.Map(
    location=[35.681382,139.76608399999998],
    zoom_start=10
  )

  # add geojson
  folium.GeoJson(
    geojson_path,
    name="首都圏",
    style_function=style_function
  ).add_to(m)

  m.save(os.path.join(save_path, 'choropleth2.html'))
  print("Created")

def gen_choropleth(json_path, number_of_city, save_path):
  noc_df = pd.read_csv(number_of_city)

  # folium init
  m = folium.Map(
    location=[35.681382,139.76608399999998],
    zoom_start=10
  )

  m.choropleth(
    geo_data=json_path,
    name='choropleth',
    data=noc_df,
    fill_opacity=0.7,
    line_opacity=0.2,
    key_on='feature.properties.N03_004',
    columns=['city', 'number'],
    threshold_scale=[0, 3,5, 7, 100],
    fill_color='YlOrRd',
    reset=True
  )

  folium.LayerControl().add_to(m)
  m.save(os.path.join(save_path, 'choropleth.html'))

def get_color(geojson):
  value = map_dict.get(geojson['feature']['properties']['N03_004'])
  if value is None:
    return '#8c8c8c' # MISSING -> gray
  else:
    return color_scale(value)

# json用プリンター
def jprint(data):
  print(json.dumps(data, indent=2))

# 市区町村ごとのユーザ数をカウント
def counter(data_path):
  df = pd.read_csv(data_path)
  print(df)