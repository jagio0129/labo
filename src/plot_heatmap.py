# coding: UTF-8
import time
import os
import configparser
import pandas as pd
import numpy as np
from collections import defaultdict
import csv

from lib import utils
from lib.Viewer import heatmap
from lib.DataProvider import test_data
from lib.DataProvider import geo

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH     = c["GRAVITY_PATH"] + "/default"
OD_PREFECTURE_PATH  = c["OD_PREFECTURE_PATH"]
GEO_JSON         = c["GEO_JSON"]
TEST_DATA        = [GRAVITY_PATH + "/gravity_param-od-2013-07-01.csv"]

def main(gravity_path, a4d4_f, tags):
  # for abs_file in utils.file_list(gravity_path): # 実データ用
  for abs_file in TEST_DATA:  # テスト用
    print(abs_file)

    df = pd.read_csv(abs_file)
    if a4d4_f:
      df = df[(df.amount > 4) & (df.distance > 4)]
    print(df.loc[:,['origin','destination', 'amount']])

    heatmap.plot_heatmap(df, 'amount', 'origin', 'destination')
    
    date_name = utils.file_date(abs_file)
    outpath = c["DATA_PATH"] + "/gravity_heatmap" + tags
    
    heatmap.export_pdf(outpath,date_name)

def default():
  gravity_data = c["GRAVITY_PATH"] + "/default"
  a4d4_f = False
  tags = "/default"
  main(gravity_data,a4d4_f,tags)

def a4d4():
  gravity_data = c["GRAVITY_PATH"] + "/default"
  a4d4_f = True
  tags = "/a4d4"
  main(gravity_data,a4d4_f,tags)

def one_point():
  gravity_data = c["GRAVITY_PATH"] + "/one_point"
  a4d4_f = False
  tags = "/one_point"
  main(gravity_data,a4d4_f,tags)

def onepoint_a4d4():
  gravity_data = c["GRAVITY_PATH"] + "/one_point"
  a4d4_f = True
  tags = "/onepoint_a4d4"
  main(gravity_data,a4d4_f,tags)

# 全日データを用いてヒートマップを作成
def all_day():
  all_df = utils.all_df(GRAVITY_PATH)
  print(all_df.loc[:,['origin','destination', 'amount']])

  heatmap.plot_heatmap(all_df, 'amount', 'origin', 'destination')
  
  date_name = 'all_day'
  outpath = c["DATA_PATH"] + "/gravity_heatmap" + '/all_day'
  
  heatmap.export_pdf(outpath,date_name)

# 都道府県別にヒートマップを作成する
class Prefecture:

  # csvデータを作成する
  @classmethod
  def create(cls):
    # for abs_file in utils.file_list(gravity_path): # 実データ用
    for abs_file in TEST_DATA:  # テスト用
      df = pd.read_csv(abs_file)
      geo_json = utils.json_parser(GEO_JSON)  # GeoJSONをロード
      od_counter = defaultdict(int)

      for index, row in df.iterrows():
        ori_pref = geo.prefecture(geo_json, row.origin_id)
        des_pref = geo.prefecture(geo_json, row.destination_id)
        amount = row.amount

        od_counter[str(ori_pref) + "=>" + str(des_pref)] += amount
      
      # CSVファイルとして保存する
      date_name = utils.file_date(abs_file)
      outpath = OD_PREFECTURE_PATH + "/heatmap-" + date_name + ".csv" # save path
      header = ['origin', 'destination', 'amount']     # csv header

      with open(outpath,'w') as f:
        w = csv.writer(f)
        w.writerow(header) # ヘッダーを書き込む
        for key in od_counter.keys():
          od_city_ary = key.split("=>")
          origin = od_city_ary[0]
          destination = od_city_ary[1]
          f.write("%s,%s,%s\n" % (origin, destination, od_counter[key]))
    
  @classmethod
  def run(cls):
    for abs_file in utils.file_list(OD_PREFECTURE_PATH): # 実データ用
      print(abs_file)

      df = pd.read_csv(abs_file)
      
      heatmap.plot_pref_heatmap(df, 'amount', 'origin', 'destination')
      
      date_name = utils.file_date(abs_file)
      outpath = c["DATA_PATH"] + "/gravity_heatmap" + "/prefecture"
      
      heatmap.export_pdf(outpath,date_name)

        
if __name__ == '__main__':
  start = time.time()
  # スクリプトの概要をdump
  utils.dump_description("Plot Heat Map.")

  # all_day()
  # default()
  # a4d4()
  # one_point()
  # onepoint_a4d4()

  Prefecture.create()
  Prefecture.run()

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")