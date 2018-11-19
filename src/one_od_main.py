# coding: UTF-8

import sys
sys.dont_write_bytecode = True
import time
import os
import pandas as pd
import configparser
from collections import defaultdict
from tqdm import tqdm
import csv

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

# Data_Frameが2行かどうか
def check_2row(data_frame):
  if len(data_frame) == 2:
    return True
  False

# 先頭とその次のレコードを多値で返す
def orgin_dest(data_frame):
  new_df = data_frame[0:2]
  if not check_2row(new_df):
    print(new_df)
    raise
  return new_df.head(1), new_df.tail(1)

### main
if __name__ == '__main__':
  start = time.time()

  pd.set_option("display.max_colwidth", 1000)

  # スクリプトの概要をdump
  utils.dump_description("Create Origin-Destination CSV file of One point.")

  geo_json = utils.json_parser(GEO_JSON)
  od_counter = defaultdict(int)     # ODをカウントするためのdict

  # for abs_file in utils.file_list(PERSON_TRIP): # 実データ用
  for abs_file in TEST_DATA:  # テスト用
    # 一箇所ユーザのデータをロード
    df = pd.read_csv(abs_file)
    uList = user.stop_one_point_user_ids(df)
    
    pbar = tqdm(total=len(uList))  # for progress bar
    for u in uList:
      od_df = user.orgin_and_stay(df, u)
      
      try:
        # odデータの取得
        orgin, dest = orgin_dest(od_df)
        # 緯度経度から市区町村名を取得
        orgin_city, orgin_city_id = geo.belong(geo_json, orgin["latitude"], orgin["longitude"])
        dest_city, dest_city_id = geo.belong(geo_json, dest["latitude"], dest["longitude"])

        # 同市区町村なら処理しない
        if orgin_city == dest_city:
          continue

        # ODをカウント
        od_counter[str(orgin_city) + ":" + str(orgin_city_id) + "=>" + str(dest_city) + ":" + str(dest_city_id)] += 1
      except:
        pass
      finally:
        pbar.update(1)
    pbar.close()

    # CSVファイルとして保存する
    date_name = utils.file_date(abs_file)
    outpath = OD_PATH + "/onepoint_od-" + date_name + ".csv" # save path
    header = ['origin', 'destination', 'origin_id', 'destination_id', 'count']     # csv header

    print("Create " + outpath)
    with open(outpath,'w') as f:
      w = csv.writer(f)
      w.writerow(header) # ヘッダーを書き込む
      for key in od_counter.keys():
        od_city_ary = key.split("=>")
        origin = od_city_ary[0].split(":")
        destination = od_city_ary[1].split(":")
        f.write("%s,%s,%s,%s,%s\n"%(origin[0],destination[0],origin[1],destination[1],od_counter[key]))
      
  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

