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
from lib.DataProvider import test_data
from lib.DataProvider import fitter
from lib.Viewer import ploter

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

# データをプロット
def default(x, y):
  # プロット設定
  ploter.init(title="test", xlabel="x", ylabel="y")
  plt.scatter(x, y, s=1)

# データをログスケールでプロット
def logscale(x, y):
  default(x, y)
  plt.xscale("log")
  plt.yscale("log")

# データとフィッティング線をプロット
def data_fit(x, y):
  default(x, y)

  # べき関数でfit
  logx, logy = np.log(x), np.log(y)
  b, a = fitter.Original.fit(logx, logy)
  a = math.e ** a
  plt.plot(x, fitter.pow_func(x, a, b), "r-")

# データとフィッティング線をログススケールでプロット
def logscale_data_fit(x, y):
  data_fit(x, y)
  plt.xscale("log")
  plt.yscale("log")

def main():
  
  ### データ準備

  # 保存先の定義
  date_name = utils.file_date(abs_file)
  outpath = c["GRAVITY_PATH"] + "/img" + gravity_data
  
  # csv load
  df = pd.read_csv(abs_file)  
  # x軸に対して昇順ソートしないと正しくフィットさせられない
  df = df.sort_values("distance")
  x, y = df.distance, df.amount

  ### プロット
  default(x,y)
  ploter.export(outpath + "/default", date_name)

  logscale(x,y)
  ploter.export(outpath + "/logscale", date_name)

  data_fit(x,y)
  ploter.export(outpath + "/powfit", date_name)

  logscale_data_fit(x,y)
  ploter.export(outpath + "/logscale_powfit", date_name)

### main
if __name__ == '__main__':

  start = time.time()
  utils.dump_description("Plot Gravity Model data.")

  c = configparser.ConfigParser()
  c.read(SOURCE_PATH + '/config.ini')
  c = c["DEFAULT"]

  gravity_data = "/default"
  GRAVITY_PATH = c["GRAVITY_PATH"] + gravity_data
  TEST_PATH = [GRAVITY_PATH + "/gravity_param-od-2013-07-01.csv"]

  # ODデータファイルに対し以下の処理
  for abs_file in utils.file_list(GRAVITY_PATH):
  # for abs_file in TEST_PATH:
    print("Load: " + abs_file)

    main()

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

