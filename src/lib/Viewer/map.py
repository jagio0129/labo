import folium
import pandas as pd
# import os
# import branca

# folium init
def init_map():
  tokyo_station = [35.681382,139.76608399999998]
  return folium.Map(
    location=tokyo_station,
    zoom_start=10
  )

# geojsonを反映したmapをhtmlで保存
def geojson_map(geojson_path, save_path):
  print("Create GeoJson Map")
  m = init_map()

  # add geojson
  folium.GeoJson(
    geojson_path,
    name="首都圏"
  ).add_to(m)

  m.save(save_path)
  print("Created")

# コロプレスマップを表示するHTMLファイルの作成。
# NOTE: None値の処理がないので、そのままだとデータのない部分は
#       一番濃い色で塗られてしまい、データが正しく表現できない。
def choropleth_map(geojson_path, show_data, save_path):
  noc_df = pd.read_csv(show_data)

  m = init_map()

  m.choropleth(
    geo_data=geojson_path,
    name='choropleth',
    data=noc_df,
    fill_opacity=0.7,
    line_opacity=0.2,
    key_on='feature.properties.N03_004',
    columns=['city', 'number'],
    threshold_scale=[10, 30, 50, 70, 90, 110],
    fill_color='PuBuGn',
    reset=True
  )

  folium.LayerControl().add_to(m)
  m.save(save_path)

"""
# コロプレスマップを表示するHTMLファイルの作成。
def my_choropleth_map(geojson_path, show_data, save_path):
  if not os.path.isfile(save_path):
    print("Create Choropleth Map: " + save_path)
    noc_df = pd.read_csv(show_data, na_values=[' '])

    colorscale = branca.colormap.linear.PuRd_09.scale(0, 500)
    population_series = noc_df.set_index('city')['number']

    # GeoJsonの表示形式の設定
    def style_function(feature):
      population = population_series.get(str(feature['properties']['N03_004']), None)
      return {
        'fillOpacity': 0.7,
        'weight': 0,
        'fillColor': '#yellow' if population is None else colorscale(population)
      }

    # folium init
    m = init_map()

    # add geojson
    folium.GeoJson(
      geojson_path,
      name="首都圏",
      style_function=style_function
    ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save(save_path)
    print("Created")
"""