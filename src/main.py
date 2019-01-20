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

  # スクリプトの概要をdump
  utils.dump_description("Create Origin-Destination CSV file.")
  
  for abs_file in utils.file_list(PERSON_TRIP): # 実データ用
  # for abs_file in TEST_DATA:  # テスト用
    print("Load: " + abs_file)

    df = pd.read_csv(abs_file)
    print(len(df))