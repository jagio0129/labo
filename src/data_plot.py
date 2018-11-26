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

from lib import utils
from lib.Viewer import ploter

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH = c["GRAVITY_PATH"]
GRAVITY_IMAGE_PATH = GRAVITY_PATH + "/img"

class TestData():
  # 指数関数
  @classmethod
  def exp_bias(cls, x):
    return np.exp(x/20)

  # べき関数
  @classmethod
  def pow_bias(cls, x):
    return pow(x, 2)

  # テストデータ(x,y)を生成。
  #   num : 生成するデータの個数
  #   bias : データを生成するのに使用する関数("exp":指数関数、"pow":べき関数)
  #   margin : ランダムで誤差をつくるためのしきい値
  @classmethod
  def create(cls, bias :str, num=100, margin=0):
    x, y = list(), list()
    for v in range(num):
      x.append(v)
      y.append(eval("cls.%s_bias(v)" % bias))
    # yに誤差を発生させる
    y = [v + int(v/10) * random.randint(-margin, margin) for v in y]
    # yに対してソートする
    # y = sorted(y)
    return np.array(x), np.array(y)

class Plot:

  def __init__(self, title="TEST", xlabel="Distance", ylabel="Amount"):
    self.title   = title
    self.xlabel  = xlabel
    self.ylabel  = ylabel

  # データをプロットし保存
  def default(self, x, y, filename="default", savedir="./"):
    ploter.plot(x, y, self.title, self.xlabel, self.ylabel)
    ploter.export(savedir, filename)

  # データと指数関数式をプロットし保存
  def exp(self, x, y, filename="default", savedir="./"):
    ploter.plot(x, y, self.title, self.xlabel, self.ylabel)
    plt.plot(x, TestData.exp_bias(x), linestyle='dashed', color="green", linewidth = 3.0, label='line1')
    ploter.export(savedir, filename)

  # データとべき関数式をプロットし保存
  def pow(self, x, y, filename="default", savedir="./"):
    ploter.plot(x, y, self.title, self.xlabel, self.ylabel)
    plt.plot(x, TestData.pow_bias(x), linestyle='dashed', color="green", linewidth = 3.0, label='line1')
    ploter.export(savedir, filename)

  # データ、指数関数フィッティング線をプロットして保存
  def exp_fit(self, x, y, filename="default", savedir="./"):
    ploter.plot(x, y, self.title, self.xlabel, self.ylabel)
    ploter.exp_fit(x, y)
    ploter.export(savedir, filename)

  # データ、べき関数フィッティング線をプロットして保存
  def pow_fit(self, x, y, filename="default", savedir="./"):
    ploter.plot(x, y, self.title, self.xlabel, self.ylabel)
    ploter.pow_fit(x, y)
    ploter.export(savedir, filename)

  # データ、指数関数、フィッティング線をプロットして保存
  def exp_fit_with_fomula(self, x, y, filename="default", savedir="./"):
    ploter.plot(x, y, self.title, self.xlabel, self.ylabel)
    ploter.exp_fit(x, y)
    plt.plot(x, TestData.exp_bias(x), linestyle='dashed', color="green", linewidth = 3.0, label='line1')
    ploter.export(savedir, filename)

  # データ、べき関数、フィッティング線をプロットして保存
  def pow_fit_with_fomula(self, x, y, filename="default", savedir="./"):
    ploter.plot(x, y, self.title, self.xlabel, self.ylabel)
    ploter.pow_fit(x, y)
    plt.plot(x, TestData.pow_bias(x), linestyle='dashed', color="green", linewidth = 3.0, label='line1')
    ploter.export(savedir, filename)

class LogScalePlot:

  def __init__(self, title="TEST", xlabel="Distance", ylabel="Amount"):
    self.title   = title
    self.xlabel  = xlabel
    self.ylabel  = ylabel    
  
  # 片対数スケールにして、データを表示
  def single(self, x, y, filename="default", savedir="./"):
    ploter.single_log_plot(x, y, self.title, self.xlabel, self.ylabel)
    ploter.export(savedir, filename)
  
  # 片対数スケールにして、データとフィッティング線を表示
  def single_fit(self, x, y, filename="default", savedir="./"):
    ploter.single_log_plot(x, y, self.title, self.xlabel, self.ylabel)
    ploter.exp_fit(x, y)
    ploter.export(savedir, filename)

  # 両対数スケールにして、データを表示
  def multi(self, x, y, filename="default", savedir="./"):
    ploter.multi_log_plot(x, y, self.title, self.xlabel, self.ylabel)
    ploter.export(savedir, filename)

  # 両対数スケールにして、データとフィッティング線を表示
  def multi_fit(self, x, y, filename="default", savedir="./"):
    ploter.multi_log_plot(x, y, self.title, self.xlabel, self.ylabel)
    ploter.pow_fit(x, y)
    ploter.export(savedir, filename)

# 人口を１万で割る
def divide_ten_thousond(pop):
  return round(pop / 10000, 3)

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
    # x = df.distance
    # y = df.amount

    methods = ["exp", "pow"]
    for method in methods:
        
      # テストデータ
      x, y = TestData.create(method, 100, 5)

      folder = method
      
      p = Plot("Test")
      p.default(x, y, "default-%s" % folder, folder)
      exec("p.%s_fit(x, y, 'fit-%s', folder)" % (folder, folder))
      exec("p.%s_fit_with_fomula(x, y, 'fit-%s-with-fomula', folder)" % (folder, folder))

      logp = LogScalePlot("Test")
      logp.single(x, y, "single-%s" % folder, folder)
      logp.single_fit(x, y, "single-fit-%s" % folder, folder)
      logp.multi(x, y, "multi-%s" % folder, folder)
      logp.multi_fit(x, y, "multi-fit-%s" % folder, folder)

      #plot_fit(x, y, "prod-with-fit-pow", "prod")
      #multi_log_plot_fit(x, y, "prod-log-fit-pow", "prod")
    
  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

