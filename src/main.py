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

from lib import utils
from lib.DataProvider import user
from lib.DataProvider import geo
from lib.DataProvider import date
from lib.Viewer import map as mymap

### files
# 2013-07-01.csv, 2013-07-07.csv, 2013-10-07.csv,
# 2013-10-13.csv, 2013-12-16.csv, 2013-12-22.csv

FOLDER = "/home/vagrant/mount_folder/lab/data/person_trip"
TEST_FOLDER = ["/home/vagrant/mount_folder/lab/data/person_trip/2013-07-01.csv"]
GEO_JSON = "/home/vagrant/mount_folder/lab/data/geojson/syutoken.geojson"
SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))
CHOROPLETH_DATA = SOURCE_PATH + "/number_of_city_15.csv"
TIME_RANGE = 11

def initializer(abs_file):
  # メッシュコードを追加したDataFrameをロード
  df = geo.gen_mesh_csv(abs_file, FOLDER)
  # 時間をdatetime型にキャスト
  df['date'] = pd.to_datetime(df['date'])

  # 一時間ごと24個のDateTimeオブジェクトを生成
  file = os.path.basename(abs_file)
  byH = date.gen_by_date(
    utils.file_date(file),
    24,
    "H"
  )

  return df, byH


### main
if __name__ == '__main__':
  start = time.time()

  os.chdir(FOLDER)
  
  #for abs_file in utils.file_list(FOLDER): # 実データ用
  for abs_file in TEST_FOLDER:  # テスト用
    print("File: " + abs_file)
    df, byH = initializer(abs_file)
    
    # 指定期間の最初のレコードのみを取得
    extra_df = date.get_first_data(df, byH[TIME_RANGE], user.user_list(df))
    # インデックスをintに変更
    extra_df.index = range(1,len(extra_df)+1)
    # コロプレスマップ用のデータを作成
    geo.gen_chotopleth_data(extra_df, CHOROPLETH_DATA, GEO_JSON)
    # コロプレスマップを表示するHTMLファイルの作成
    mymap.my_choropleth_map(GEO_JSON, CHOROPLETH_DATA, SOURCE_PATH)

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")