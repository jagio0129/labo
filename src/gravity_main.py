# coding: UTF-8

import os
import time
import pandas as pd
from tqdm import tqdm
import configparser
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

from lib import utils
from lib.DataProvider import gravity

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

POPULATION_SAVE_PATH = c["POPULATION_SAVE_PATH"]
OD_PATH = c["OD_PATH"]

# cityIDの人口を取得する
def population(city_id):
  if city_id == str(None):
    return None

  # 人口データをロード
  df = pd.read_csv(POPULATION_SAVE_PATH)

  for index, row in df.iterrows():
    if int(city_id) == int(row["city_id"]):
      return row["population"]
  return None

### main
if __name__ == '__main__':
  start = time.time()
  utils.dump_description("Calc Gravity Model.")

  # ODデータファイルに対し以下の処理
  for abs_file in utils.file_list(OD_PATH):
    print("Load: " + abs_file)

    df = pd.read_csv(abs_file)
    for index, row in df.iterrows():
      origin    = row["origin"]         # 始点
      origin_id = row["origin_id"]      # 始点ID
      dest      = row["destination"]    # 終点
      dest_id   = row["destination_id"] # 終点ID
      
      amount  = row["count"]          # 移動量
      distAB  = row["distance"]       # ２点間の距離
      popA    = population(origin_id) # 始点の人口
      popB    = population(dest_id)   # 終点の人口

      # グラビティモデルにおけるパラメータを計算
      param = gravity.param_fomuola(amount, popA, popB, distAB)
      print("parameter: ", param)
      raise
      
  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
