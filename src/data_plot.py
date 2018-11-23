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

from lib import utils
from lib.Viewer import ploter

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH = c["GRAVITY_PATH"]
GRAVITY_IMAGE_PATH = GRAVITY_PATH + "/img"
METHODS = ["plot", "single_log_plot", "multi_log_plot"]

# 人口を１万で割る
def divide_ten_thousond(pop):
  return round(pop / 10000, 3)

# データをプロットし保存
def plot(x, y, filename="default", savedir="./"):
  ploter.plot(x, y, "TEST", "Distance", "Amount")
  ploter.export(savedir, filename)

# データとフィッティング線をプロットし保存
def plot_fit(x, y, filename="default", savedir="./"):
  ploter.plot(x, y, "TEST", "Distance", "Amount")
  ploter.pow_fit(x, y)
  ploter.export(savedir, filename)

# データとデータのもとも式をプロット
def plot_bias(x, y, filename="default", savedir="./"):
  ploter.plot(x, y, "TEST", "Distance", "Amount")
  plt.plot(x, bias(x), linestyle='dashed', color="green", linewidth = 3.0, label='line1')
  ploter.export(savedir, filename)

# 全部出力
def plot_bias_fit(x, y, filename="default", savedir="./"):
  ploter.plot(x, y, "TEST", "Distance", "Amount")
  ploter.exp_fit(x, y)
  plt.plot(x, bias(x), linestyle='dashed', color="green", linewidth = 3.0, label='line1')
  ploter.export(savedir, filename)

# 片対数
def single_log_plot(x, y, filename="default", savedir="./"):
  ploter.single_log_plot(x, y, "TEST", "Distance", "Amount")
  ploter.export(savedir, filename)

def single_log_plot_fit(x, y, filename="default", savedir="./"):
  ploter.single_log_plot(x, y, "TEST", "Distance", "Amount")
  ploter.exp_fit(x, y)
  ploter.export(savedir, filename)

# 両対数
def multi_log_plot(x, y, filename="default", savedir="./"):
  ploter.multi_log_plot(x, y, "TEST", "Distance", "Amount")
  ploter.export(savedir, filename)

def multi_log_plot_fit(x, y, filename="default", savedir="./"):
  ploter.multi_log_plot(x, y, "TEST", "Distance", "Amount")
  ploter.pow_fit(x, y)
  ploter.export(savedir, filename) 


def bias(x):
  return np.exp(x/20)

# marginはランダムで誤差をつくるためのしきい値
def test_data(margin=0):
  x, y = list(), list()
  for v in range(100):
    x.append(v)
    y.append(bias(random.randint(v-margin, v+margin)))
  return np.array(x), np.array(y)
    
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
    
    # date_name   = utils.file_date(abs_file)
    x = df.distance
    y = df.amount
    
    plot_fit(x, y, "prod-with-fit-pow", "prod")
    multi_log_plot_fit(x, y, "prod-log-fit-pow", "prod")
    
  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

