# coding: UTF-8

import os
from tqdm import tqdm
import pandas as pd
from collections import defaultdict
from shapely.geometry import shape, Point
from lib import utils
import time
import json

# コロプレスマップ用のデータを作成する。
def gen_chotopleth_data(data_frame, choropleth_data_path, geo_json_path):
  if not os.path.isfile(choropleth_data_path):
    print("Create " + choropleth_data_path)

    city_dict = defaultdict(int)  # 区間にどのくらいのユーザがいるか格納するdict
    geo_json = utils.json_parser(geo_json_path)
    
    # DataFrame一行ずつループ
    pbar = tqdm(total=len(data_frame))
    for row in data_frame.itertuples():
      # 位置情報から市区町村名を取得
      city = belong(geo_json, row.latitude, row.longitude)
      city_dict[city] += 1
      pbar.update(1)
    pbar.close()

    # dict型をDataFrame型にキャスト
    city_df = pd.DataFrame(list(city_dict.items()),columns=['city','number'])
    # データをcsvファイルとして出力
    city_df.to_csv(choropleth_data_path)
  else:
    print("Skip create " + choropleth_data_path)

# choropleth dataに含まれるgeo_jsonだけを抽出
def gen_choropleth_json(geo_json_path, choropleth_data_path):
  print("create choropleth GeoJSON ...")
  
  geo_json = utils.json_parser(geo_json_path)
  df = pd.read_csv(choropleth_data_path)
  city_ary = []
  
  for feature in geo_json['features']:
    for row in df.itertuples():
      if feature['properties']['N03_004'] == row.city:
        city_ary.append(feature)
        break

  j = {
    "type": "FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::6668" }},
    "features" : city_ary
  }
  
  return j

# 任意の位置情報がどの市区町村に属するか判定するメソッド
def belong(json, lat, lon):
  point = Point(lon, lat)
  for feature in json['features']:
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        return feature['properties']['N03_004']
  return None