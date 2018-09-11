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

from lib import utils
from lib.DataProvider import user
from lib.DataProvider import geo
from lib.DataProvider import date
from lib.DataProvider import facility as fc
from lib.Viewer import map as mymap

### files
# 2013-07-01.csv, 2013-07-07.csv, 2013-10-07.csv,
# 2013-10-13.csv, 2013-12-16.csv, 2013-12-22.csv

ROOT_PATH = "/home/vagrant/mount_folder/lab"
DATA_PATH = ROOT_PATH + "/data"
PERSON_TRIP = DATA_PATH + "/person_trip"
CHOROPLETH = DATA_PATH + "/choropleth"
GEO_JSON = DATA_PATH + "/geojson/syutoken.geojson"
SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

TEST_FOLDER = [PERSON_TRIP + "/2013-07-01.csv"]

def initializer(abs_file):
  # メッシュコードを追加したDataFrameをロード
  df = geo.gen_mesh_csv(abs_file, PERSON_TRIP)
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

  os.chdir(PERSON_TRIP)
  
  # for abs_file in utils.file_list(PERSON_TRIP): # 実データ用
  for abs_file in TEST_FOLDER:  # テスト用
    print("File: " + abs_file)
    df, byH = initializer(abs_file)

    print(fc.facility_list(df))

    
  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
