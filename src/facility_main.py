# coding: UTF-8

import sys
sys.dont_write_bytecode = True
import pandas as pd
import time
import os
import configparser

from lib import utils
from lib.DataProvider import facility as fc

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

PERSON_TRIP = c["PERSON_TRIP"]
GEO_JSON    = c["GEO_JSON"]

TEST_DATA = [c["TEST_DATA"]]

### main
if __name__ == '__main__':
  start = time.time()

  # for abs_file in utils.file_list(PERSON_TRIP): # 実データ用
  for abs_file in TEST_DATA:  # テスト用
    print("File: " + abs_file)

    # csvファイルをDataFrameとしてロード
    df = pd.read_csv(abs_file)
    print(fc.facility_rate(df))

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
