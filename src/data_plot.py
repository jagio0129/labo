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
def plot(x, y):
  # プロット設定
  ploter.init(title="test", xlabel="x", ylabel="y")
  plt.scatter(x, y, s=1)

# データをログスケールでプロット
def logscale(x, y):
  plot(x, y)
  plt.xscale("log")
  plt.yscale("log")

# データとフィッティング線をプロット
def data_fit(x, y):
  plot(x, y)

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

class Main:

  # バイアスの無いデータ
  def default(self):

    utils.dump_description("Plot Gravity Model data.")

    gravity_data = "/default"
    GRAVITY_PATH = c["GRAVITY_PATH"] + gravity_data
    TEST_PATH = [GRAVITY_PATH + "/gravity_param-od-2013-07-01.csv"]

    for abs_file in utils.file_list(GRAVITY_PATH):
    # for abs_file in TEST_PATH:
      print("Load: " + abs_file)

      ### データ準備

      # 保存先の定義
      date_name = utils.file_date(abs_file)
      outpath = c["GRAVITY_PATH"] + "/img" + "/default"
      
      # csv load
      df = pd.read_csv(abs_file)  
      # x軸に対して昇順ソートしないと正しくフィットさせられない
      df = df.sort_values("distance")
      x, y = df.distance.values, df.amount.values

      ### プロット
      plot(x,y)
      ploter.export(outpath + "/default", date_name)

      logscale(x,y)
      ploter.export(outpath + "/logscale", date_name)

      data_fit(x,y)
      ploter.export(outpath + "/powfit", date_name)

      logscale_data_fit(x,y)
      ploter.export(outpath + "/logscale_powfit", date_name)

  # 移動量4、距離4以上のユーザのみ
  def a4d4(self):

    utils.dump_description("Plot amount & distance over 4 Gravity Model data.")

    gravity_data = "/default"
    GRAVITY_PATH = c["GRAVITY_PATH"] + gravity_data
    TEST_PATH = [GRAVITY_PATH + "/gravity_param-od-2013-07-01.csv"]

    for abs_file in utils.file_list(GRAVITY_PATH):
    # for abs_file in TEST_PATH:
      print("Load: " + abs_file)
    
      ### データ準備

      # 保存先の定義
      date_name = utils.file_date(abs_file)
      outpath = c["GRAVITY_PATH"] + "/img" + "/a4d4"
      
      # csv load
      df = pd.read_csv(abs_file)  
      # 移動量4以上、距離4以上だけ抽出
      df = df[(df.amount > 4) & (df.distance > 4)]
      # x軸に対して昇順ソートしないと正しくフィットさせられない
      df = df.sort_values("distance")
      x, y = df.distance.values, df.amount.values

      ### プロット
      plot(x,y)
      ploter.export(outpath + "/default", date_name)

      logscale(x,y)
      ploter.export(outpath + "/logscale", date_name)

      data_fit(x,y)
      ploter.export(outpath + "/powfit", date_name)

      logscale_data_fit(x,y)
      ploter.export(outpath + "/logscale_powfit", date_name)

  # 一日に一箇所だけ訪れるユーザのみ
  def one_point(self):

    utils.dump_description("Plot one destination user Gravity Model data.")

    gravity_data = "/one_point"
    GRAVITY_PATH = c["GRAVITY_PATH"] + gravity_data
    TEST_PATH = [GRAVITY_PATH + "/gravity_param-onepoint_od-2013-07-01.csv"]

    for abs_file in utils.file_list(GRAVITY_PATH):
    # for abs_file in TEST_PATH:
      print("Load: " + abs_file)

      ### データ準備

      # 保存先の定義
      date_name = utils.file_date(abs_file)
      outpath = c["GRAVITY_PATH"] + "/img" + "/one_point"
      
      # csv load
      df = pd.read_csv(abs_file)  
      # x軸に対して昇順ソートしないと正しくフィットさせられない
      df = df.sort_values("distance")
      x, y = df.distance.values, df.amount.values

      ### プロット
      plot(x,y)
      ploter.export(outpath + "/default", date_name)

      logscale(x,y)
      ploter.export(outpath + "/logscale", date_name)

      data_fit(x,y)
      ploter.export(outpath + "/powfit", date_name)

      logscale_data_fit(x,y)
      ploter.export(outpath + "/logscale_powfit", date_name)
  
  # 一日に一箇所だけ訪れるユーザから移動量4、距離4のユーザのみ
  def onepoint_a4d4(self):

    utils.dump_description("Plot one destination and amount & distance over 4 user Gravity Model data.")

    gravity_data = "/one_point"
    GRAVITY_PATH = c["GRAVITY_PATH"] + gravity_data
    TEST_PATH = [GRAVITY_PATH + "/gravity_param-onepoint_od-2013-07-01.csv"]

    for abs_file in utils.file_list(GRAVITY_PATH):
    # for abs_file in TEST_PATH:
      print("Load: " + abs_file)

      ### データ準備

      # 保存先の定義
      date_name = utils.file_date(abs_file)
      outpath = c["GRAVITY_PATH"] + "/img" + "/onepoint_a4d4"
      
      # csv load
      df = pd.read_csv(abs_file) 
      # 移動量4以上、距離4以上だけ抽出
      df = df[(df.amount > 4) & (df.distance > 4)] 
      # x軸に対して昇順ソートしないと正しくフィットさせられない
      df = df.sort_values("distance")
      x, y = df.distance.values, df.amount.values

      ### プロット
      plot(x,y)
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

  c = configparser.ConfigParser()
  c.read(SOURCE_PATH + '/config.ini')
  c = c["DEFAULT"]

  m = Main()
  m.default()
  m.a4d4()
  m.one_point()
  m.onepoint_a4d4()

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

