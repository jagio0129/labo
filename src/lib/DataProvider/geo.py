# coding: UTF-8

import jpgrid
from tqdm import tqdm
import geocoder
import os
from collections import defaultdict
import pandas as pd
from lib import utils
from shapely.geometry import shape, Point
import time

# 緯度経度からメッシュコードに換算しdfに追加して返す(1次=4桁、2次=6桁、3次=8桁)
## return <DataFrame>
def add_meshcode_column(data_frame):
  print("  Calculating mesh code...")
  pbar = tqdm(total=len(data_frame))  # for progress bar
  for index, row in data_frame.iterrows():
    mc3 = jpgrid.encodeLv3(row["latitude"], row["longitude"])
    data_frame.at[index, "mesh_code_lv1"] = mc3[:4]
    data_frame.at[index, "mesh_code_lv2"] = mc3[:6]
    data_frame.at[index, "mesh_code_lv3"] = mc3
    pbar.update(1)

  pbar.close()
  return data_frame

# 各メッシュコードのユーザがどのくらいいるかチェック
def mesh_counter(data_frame, time_range, lv):
  if (lv == 1 or lv == 2 or lv == 3):
    mask = (data_frame['date'] >= time_range) & (data_frame['date'] < time_range+1)
    data_frame = data_frame.loc[mask]
    h = "mesh_code_lv" + str(lv)
    return data_frame[h].value_counts()
  else:
    raise "lvの値が不正"

# 緯度経度から市区町村名を取得
def get_city_form_geocoder(latitude, longitude, cnt):
  if cnt > 10:
    raise "cntは10以下の整数を設置"
  g = geocoder.google([latitude, longitude], method='reverse', language="ja")
  # Noneが帰ってきたらmax10回まで
  if not g.city == None:
    return g.city
  cnt += 1
  if cnt == 10:
    return None
  return get_city_form_geocoder(latitude, longitude, cnt)

# コロプレスマップ用のデータを作成する。
def gen_chotopleth_data(data_frame, choropleth_data_path, geo_json):
  if not os.path.isfile(choropleth_data_path):
    print("Create " + choropleth_data_path)
    city_dict = defaultdict(int)
    json = utils.json_parser(geo_json)
    
    # DataFrame一行ずつループ
    pbar = tqdm(total=len(data_frame))
    for row in data_frame.itertuples():
      # 位置情報から市区町村名を取得
      city = isContains(json, row.latitude, row.longitude)
      city_dict[city] += 1
      pbar.update(1)
    pbar.close()

    # dict型をDataFrame型にキャスト
    city_df = pd.DataFrame(list(city_dict.items()),columns=['city','number'])
    # データをcsvファイルとして出力
    city_df.to_csv(choropleth_data_path)
  else:
    print("Skip create " + choropleth_data_path)

# メッシュコードを追加した新規CSVファイルを生成する。
#   return <DataFrame>
def gen_mesh_csv(abs_file, folder):
  suffix = "_onMesh.csv"
  file = os.path.basename(abs_file)
  root, ext = os.path.splitext(file)
  new_file = folder + "/" + root + suffix
  if os.path.isfile(new_file):
    print("Skip create " + new_file)
    return pd.read_csv(new_file)
  else:
    print("Create " + new_file)
    df = pd.read_csv(abs_file)
    df = add_meshcode_column(df)
    return df.to_csv(new_file, index=False)

# 任意の位置情報がどの市区町村に属するか判定するメソッド
def isContains(json, lat, lon):
  point = Point(lon, lat)
  for feature in json['features']:
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        return feature['properties']['N03_004']
  return None
