# coding: UTF-8

import pandas as pd
import time
import os
import configparser
from tqdm import tqdm

from lib import utils
from lib.DataProvider import gravity
from lib.DataProvider import geo

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

PERSON_TRIP = c["PERSON_TRIP"]
GEO_JSON    = c["GEO_JSON"]
TEST_DATA   = [c["TEST_DATA"]]
OD_PATH     = c["OD_PATH"]
PUBOFFICE_PATH   = c["PUBOFFICE_PATH"]

### main
if __name__ == '__main__':
  start = time.time()

  # スクリプトの概要をdump
  utils.dump_description("Calcurate 2 point distance.")

  for abs_file in utils.file_list(OD_PATH): # 実データ用
  # for abs_file in TEST_DATA:  # テスト用
    print("Load: " + abs_file)

    od_df = pd.read_csv(abs_file)
    # ヘッダーにdistanceが存在していれば次
    if 'distance' in od_df.columns.values:
      print("'distance' header exists.")
      continue
    od_df["distance"] = 0.0
      
    # ODデータに対して以下の処理を行う
    pbar = tqdm(total=len(od_df))  # for progress bar   
    for index, od_row in od_df.iterrows():
      # originとdestinationの市区町村名IDを取得
      origin, dest = od_row["origin"], od_row["destination"]
      origin_id, dest_id = od_row["origin_id"], od_row["destination_id"]
      if (origin_id == str(None)) or (dest_id == str(None)):
        continue
      
      # 位置情報を取得
      origin_latlon = geo.puboffice_latlon(PUBOFFICE_PATH, origin_id)
      dest_latlon   = geo.puboffice_latlon(PUBOFFICE_PATH, dest_id)

      # 距離を算出
      dist = gravity.dist_on_sphere(origin_latlon, dest_latlon)
      
      # ODデータに距離を追加
      od_df.ix[[index],["distance"]] = dist

      pbar.update(1)
    pbar.close()

    # csvファイルとして保存
    od_df.to_csv(abs_file, index=False)
   
  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
