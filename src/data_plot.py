# coding: UTF-8

import configparser
import os
import time
import numpy as np
import matplotlib
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
import pandas as pd
import random
from operator import itemgetter
import math

from lib import utils
from lib.Viewer import ploter

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH = c["GRAVITY_PATH"]
GRAVITY_IMAGE_PATH = GRAVITY_PATH + "/img"

### main
if __name__ == '__main__':
  start = time.time()
  utils.dump_description("Plot Gravity Model data.")

  GRAVITY_PATH += "/default"
  # テスト用
  TEST_PATH = [GRAVITY_PATH + "/gravity_param-od-2013-07-01.csv"]
  
  # ODデータファイルに対し以下の処理
  # for abs_file in utils.file_list(GRAVITY_PATH):
  for abs_file in TEST_PATH:
    print("Load: " + abs_file)

    # csv load
    df = pd.read_csv(abs_file)
    
    # x軸に対して昇順ソートしないと正しくフィットさせられない
    df = df.sort_values("distance")
    
    date_name = utils.file_date(abs_file)
    
    x = df.distance
    y = df.amount

    outpath = "./test1_log.png"

    plt.scatter(x,y, s=1)

    ploter.Numpy.liner_fit(x,y)    
    plt.savefig(outpath)

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

