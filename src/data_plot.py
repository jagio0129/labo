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

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH = c["GRAVITY_PATH"]
GRAVITY_IMAGE_PATH = GRAVITY_PATH + "/img"

# 人口を１万で割る
def divide_ten_thousond(pop):
  return round(pop / 10000, 3)

# plot画像を生成する。
def save_png(path, dir, tag, plt):
  
  # save path
  date_name = utils.file_date(abs_file)
  outpath = GRAVITY_IMAGE_PATH + "/" + dir + "/"+ tag + "/" + date_name + ".png"
  file_path = os.path.dirname(outpath)
  print("Create " + outpath)
  
  # ディレクトリが存在しなければ生成
  if not os.path.exists(file_path):
    os.makedirs(file_path)

  plt.savefig(outpath)

# x:距離、 y:移動量でプロット
def plot(data_frame, path, dir="default"):
  # データの用意
  # origin_pop  = list(map(optimize, df["origin_pop"].values))
  # dest_pop    = list(map(optimize, df["dest_pop"].values))
  distance    = data_frame["distance"].values
  amount      = data_frame['amount'].values
  # r           = df['right_fomula'].values

  # figure
  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)

  # 散布図 config
  ## sはドットの太さ。markerでドット文字を変更できる
  ax.scatter(distance, amount, s=1)
      
  # general config
  ax.set_title('Gravity Model')
  ax.set_xlabel('DistanceAB')
  ax.set_ylabel('Amount')

  # save as png
  save_png(path, dir, "default", plt)

# 片対数計算で表示
def single_log_plot(data_frame, path):
  
  distance    = data_frame["distance"].values
  amount      = data_frame['amount'].values
  
  # figure
  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)

  # 散布図 config
  ## sはドットの太さ。markerでドット文字を変更できる
  ax.scatter(distance, amount, s=1)
      
  # general config
  ax.set_title('Gravity Model')
  ax.set_xlabel('DistanceAB')
  ax.set_ylabel('Amount')

  # log
  plt.xscale("log")

  # save as png
  save_png(path, "dist-amount", "singe-log", plt)

# 両対数グラフ
def multi_log_plot(data_frame, path):
  
  distance    = data_frame["distance"].values
  amount      = data_frame['amount'].values
  
  # figure
  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)

  # 散布図 config
  ## sはドットの太さ。markerでドット文字を変更できる
  ax.scatter(distance, amount, s=1)
      
  # general config
  ax.set_title('Gravity Model')
  ax.set_xlabel('DistanceAB')
  ax.set_ylabel('Amount')

  # log
  plt.xscale("log")
  plt.yscale("log")

  # save as png
  save_png(path, "dist-amount", "multi-log", plt)
  
### main
if __name__ == '__main__':
  start = time.time()
  utils.dump_description("Plot Gravity Model data.")

  # ODデータファイルに対し以下の処理
  for abs_file in utils.file_list(GRAVITY_PATH):
    print("Load: " + abs_file)

    # csv load
    df = pd.read_csv(abs_file)

    # 移動量4以上 かつ 距離2km以上を抽出 
    df = df[(df.amount >= 4) & (df.distance >= 2)]

    # plot 
    plot(df, abs_file, "over-a4-d2")
    # single_log_plot(df, abs_file)
    # multi_log_plot(df, abs_file)

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

