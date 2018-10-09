# coding: UTF-8

import sys
sys.dont_write_bytecode = True
import pandas as pd
import time
import os
import codecs

from lib import utils

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

PERSON_TRIP             = c["PERSON_TRIP"]
GEO_JSON                = c["GEO_JSON"]
POPULATION_ORIGIN_DATA  = c["POPULATION_ORIGIN_DATA"]
POPULATION_SAVE_PATH    = c["POPULATION_SAVE_PATH"]

TEST_DATA = [c["TEST_DATA"]]

### main
if __name__ == '__main__':
  start = time.time()

  # GeoJSONをロード
  geo_json = utils.json_parser(GEO_JSON)

  # csvファイルをDataFrameとしてロード
  with codecs.open(POPULATION_ORIGIN_DATA, "r", "Shift-JIS", "ignore") as file:
    df = pd.read_table(file, delimiter=",")

    area_stack = []
    # csvファイルの作成
    with open(POPULATION_SAVE_PATH, 'w') as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=['city', 'population'])
      writer.writeheader()
      
      # GeoJSONのデータに対して以下の処理を行う
      for feature in geo_json['features']:
        area_code = feature['properties']['N03_007']
        city_name = feature['properties']['N03_004']

        # すでに処理した地域コードなら飛ばす
        if area_code in area_stack:
          continue

        area_stack.append(area_code)

        # 「市区町村名」が「所属未定地」ならば飛ばす
        if city_name == "所属未定地":
          continue
        
        # 地域コードから人口を取得する
        area_df = df[df["地域コード"] == int(area_code)]
        # 指定した地域コードのデータがなければ処理を止める
        if len(area_df) == 0:
          raise("GeoJSONに含まれる地域の人口データが存在しません")
        
        population = area_df["人口　総数"].head(1).values[0]
        writer.writerow({'city': city_name, 'population': population})
        
  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")