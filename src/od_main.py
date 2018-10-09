# coding: UTF-8

import sys
sys.dont_write_bytecode = True
import pandas as pd
import time
import os
import configparser
from collections import defaultdict
import csv
from tqdm import tqdm

from lib import utils
from lib.DataProvider import user
from lib.DataProvider import geo

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

PERSON_TRIP = c["PERSON_TRIP"]
GEO_JSON    = c["GEO_JSON"]
TEST_DATA   = [c["TEST_DATA"]]
OD_PATH     = c["OD_PATH"]

### main
if __name__ == '__main__':
  start = time.time()

  geo_json = utils.json_parser(GEO_JSON)
  od_counter = defaultdict(int)     # ODをカウントするためのdict

  for abs_file in utils.file_list(PERSON_TRIP): # 実データ用
  # for abs_file in TEST_DATA:  # テスト用
    print("Load: " + abs_file)

    # csvファイルをDataFrameとしてロード
    df = pd.read_csv(abs_file)
    
    # ユーザデータごとに以下の処理を行う
    u_list = user.user_list(df)
    pbar = tqdm(total=len(u_list))  # for progress bar
    for u in u_list:
      # ODデータを取得
      od_df = user.get_start_end_and_stay(df, u)

      # ODレコード全てに対して処理をする
      for i in range(1, len(od_df), 1):
        orgin_df = od_df.iloc[i-1]
        next_df = od_df.iloc[1]
        
        # 緯度経度から市区町村名を取得
        orgin_city = geo.belong(geo_json, orgin_df["latitude"], orgin_df["longitude"])
        next_city = geo.belong(geo_json, next_df["latitude"], next_df["longitude"])

        # 同市区町村なら処理しない
        if orgin_city == next_city:
          continue

        # ODをカウント
        od_counter[str(orgin_city) + "=>" + str(next_city)] += 1
      pbar.update(1)
    pbar.close()

    # CSVファイルとして保存する
    date_name = utils.file_date(abs_file)
    outpath = OD_PATH + "/od-" + date_name + ".csv" # save path
    header = ['OD', 'count']          # csv header
    with open(outpath,'w') as f:
      w = csv.writer(f)
      w.writerow(header) # ヘッダーを書き込む
      for key in od_counter.keys():
        f.write("%s,%s\n"%(key,od_counter[key]))
      
  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")