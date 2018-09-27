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

### main
if __name__ == '__main__':
  start = time.time()

  # for abs_file in utils.file_list(PERSON_TRIP): # 実データ用
  for abs_file in TEST_FOLDER:  # テスト用
    print("File: " + abs_file)

    # csvファイルをDataFrameとしてロード
    df = pd.read_csv(abs_file)

    print(user.get_start_end_and_stay(df, 2000))

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")