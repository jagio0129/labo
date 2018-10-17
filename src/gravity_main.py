# coding: UTF-8

import os
import time
import pandas as pd
from tqdm import tqdm
import configparser
import csv

from lib import utils
from lib.DataProvider import gravity

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

POPULATION_SAVE_PATH = c["POPULATION_SAVE_PATH"]
OD_PATH = c["OD_PATH"]
GRAVITY_PATH = c["GRAVITY_PATH"]

HEADER = ['origin', 'destination', 'origin_id', 'destination_id', 'devided', 'devide', 'gravity_parameter']

### main
if __name__ == '__main__':
  start = time.time()
  utils.dump_description("Calc Gravity Model.")

  # ODデータファイルに対し以下の処理
  for abs_file in utils.file_list(OD_PATH):
    print("Load: " + abs_file)

    date_name = utils.file_date(abs_file)
    outpath = GRAVITY_PATH + "/gravity_param-" + date_name + ".csv" # save path
    
    # csvファイルの作成
    with open(outpath, 'w') as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=HEADER)
      writer.writeheader()

      df = pd.read_csv(abs_file)
      pbar = tqdm(total=len(df))  # for progress bar
      for index, row in df.iterrows():
        origin    = row["origin"]         # 始点
        origin_id = row["origin_id"]      # 始点ID
        dest      = row["destination"]    # 終点
        dest_id   = row["destination_id"] # 終点ID
        
        amount  = row["count"]          # 移動量
        distAB  = row["distance"]       # ２点間の距離
        popA    = gravity.population(POPULATION_SAVE_PATH, origin_id) # 始点の人口
        popB    = gravity.population(POPULATION_SAVE_PATH, dest_id)   # 終点の人口

        # グラビティモデルにおけるパラメータを計算
        try:
          devided, devide, param = gravity.param_fomuola(amount, popA, popB, distAB)
        except Exception as e:
          print(e)
          continue
        
        writer.writerow({
          'origin': origin,
          'destination':dest,
          'origin_id': origin_id,
          'destination_id': dest_id,
          'devided': devided,
          'devide': devide,
          'gravity_parameter': str(param)
        })
        pbar.update(1)
      pbar.close()
      
  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
