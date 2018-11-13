# coding: UTF-8

import configparser
import os
import time
import numpy as np
import matplotlib
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
import pandas as pd

from lib import utils
from lib.Viewer import ploter

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH = c["GRAVITY_PATH"]
GRAVITY_IMAGE_PATH = GRAVITY_PATH + "/img"

# 人口を１万で割る
def divide_ten_thousond(pop):
  return round(pop / 10000, 3)

# 最小二乗法でフィット
def fitting(xvalues, yvalues, dimension: int, color='red'):
  plt.plot(xvalues, np.poly1d(np.polyfit(xvalues, yvalues, dimension))(xvalues), color=color)

# デフォルト、片対数、両対数をまとめて実行
def all_plot(xvalues, yvalues, title, xlabel, ylabel, dir, filename):

  # プロット情報のセット
  ploter.plot(
    xvalues, 
    yvalues, 
    title,
    xlabel,
    ylabel
  )

  # 画像ファイルとして保存
  ploter.export(GRAVITY_IMAGE_PATH, dir, "simple", filename)

    # プロット情報のセット
  ploter.single_log_plot(
    xvalues, 
    yvalues, 
    title,
    xlabel,
    ylabel
  )

  # 画像ファイルとして保存
  ploter.export(GRAVITY_IMAGE_PATH, dir, "single-log", filename)

    # プロット情報のセット
  ploter.multi_log_plot(
    xvalues, 
    yvalues, 
    title,
    xlabel,
    ylabel
  )

  # 画像ファイルとして保存
  ploter.export(GRAVITY_IMAGE_PATH, dir, "multi-log", filename)

# 最小二乗法付きで実行
def all_plot_with_fit(xvalues, yvalues, title, xlabel, ylabel, dir, filename, dimension):

  # プロット情報のセット
  ploter.plot(
    xvalues, 
    yvalues, 
    title,
    xlabel,
    ylabel
  )

  fitting(xvalues, yvalues, dimension)

  # 画像ファイルとして保存
  ploter.export(GRAVITY_IMAGE_PATH, dir, "simple-%dd" % dimension, filename)

    # プロット情報のセット
  ploter.single_log_plot(
    xvalues, 
    yvalues, 
    title,
    xlabel,
    ylabel
  )

  fitting(xvalues, yvalues, dimension)

  # 画像ファイルとして保存
  ploter.export(GRAVITY_IMAGE_PATH, dir, "single-log-%dd" % dimension, filename)

    # プロット情報のセット
  ploter.multi_log_plot(
    xvalues, 
    yvalues, 
    title,
    xlabel,
    ylabel
  )

  fitting(xvalues, yvalues, dimension)

  # 画像ファイルとして保存
  ploter.export(GRAVITY_IMAGE_PATH, dir, "multi-log-%dd" % dimension, filename)


### main
if __name__ == '__main__':
  start = time.time()
  utils.dump_description("Plot Gravity Model data.")

  # ODデータファイルに対し以下の処理
  for abs_file in utils.file_list(GRAVITY_PATH):
    print("Load: " + abs_file)

    # csv load
    df = pd.read_csv(abs_file)

    distance    = df["distance"].values
    amount      = df['amount'].values
    date_name = utils.file_date(abs_file)

    all_plot(distance, amount, "GravityModel", "Distance", "Amount", "default", date_name)
    all_plot_with_fit(distance, amount, "GravityModel", "Distance", "Amount", "fitting", date_name, 2)

    # 移動量4以上 かつ 距離2km以上を抽出 
    df = df[(df.amount >= 4) & (df.distance >= 2)]

    distance    = df["distance"].values
    amount      = df['amount'].values
    
    all_plot(distance, amount, "GravityModel", "Distance", "Amount", "default-over-4a-2d", date_name)
    all_plot_with_fit(distance, amount, "GravityModel", "Distance", "Amount", "fitting-over-4a-2d", date_name, 2)

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

