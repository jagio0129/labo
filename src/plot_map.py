# coding: UTF-8

import sys
sys.dont_write_bytecode = True
import pandas as pd
import time
import os
import geocoder
from collections import defaultdict
import csv
import branca
from tqdm import tqdm
import copy
import json

from lib import utils
from lib.DataProvider import user
from lib.DataProvider import geo
from lib.DataProvider import date
from lib.Viewer import map as mymap
from lib.DataProvider import choropleth

### files
# 2013-07-01.csv, 2013-07-07.csv, 2013-10-07.csv,
# 2013-10-13.csv, 2013-12-16.csv, 2013-12-22.csv

ROOT_PATH       = "/home/vagrant/mount_folder/lab"
DATA_PATH       = ROOT_PATH + "/data"
PERSON_TRIP     = DATA_PATH + "/person_trip"
CHOROPLETH_DATA = DATA_PATH + "/choropleth/data"
CHOROPLETH_HTML = DATA_PATH + "/choropleth/html"
GEO_JSON        = DATA_PATH + "/geojson/syutoken.geojson"
SOURCE_PATH     = os.path.dirname(os.path.abspath(__file__))

TEST_FOLDER = [PERSON_TRIP + "/2013-07-01.csv"]

def mk_filnename(time_name):

  t_str = time_name.strftime("%Y-%m-%d_%H-%M-%S")
  choropleth_data = CHOROPLETH_DATA + "/" + str(t_str) + ".csv"
  save_path = CHOROPLETH_HTML + "/choropleth-" + str(t_str) + ".html" 

  return choropleth_data, save_path

### main
if __name__ == '__main__':
  start = time.time()

  # for abs_file in utils.file_list(PERSON_TRIP): # 実データ用
  for abs_file in TEST_FOLDER:  # テスト用
    print("File: " + abs_file)

    # csvファイルをDataFrameとしてロード
    df = pd.read_csv(abs_file)

    # 一時間ごと24個のDateTimeオブジェクトを生成
    file = os.path.basename(abs_file)
    byH = date.gen_by_date(
      utils.file_date(file),
      24,
      "H"
    )

    # 一時間ごとに以下を実行
    for v in byH:
    # v = byH[1] # テスト用
      choropleth_data, save_path = mk_filnename(v)
      
      # 指定期間の最初の
      # レコードのみを取得
      tmp_df = copy.deepcopy(df)
      extra_df = ""
      if not os.path.isfile(choropleth_data):
        extra_df = date.get_first_data(tmp_df, v, user.user_list(tmp_df))
      
      # コロプレスマップ用のデータを作成
      choropleth.gen_chotopleth_data(extra_df, choropleth_data, GEO_JSON)
      # コロプレスマップ用のgeojsonデータの作成
      geo_json = choropleth.gen_choropleth_json(GEO_JSON,choropleth_data)
      # コロプレスマップの作成
      mymap.choropleth_map(geo_json,choropleth_data, save_path)

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
