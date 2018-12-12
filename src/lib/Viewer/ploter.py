# coding: UTF-8

import matplotlib
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import os
import math

from lib.DataProvider import test_data

def export(path, filename="default"):
  outpath = "%s/%s.png" % (path, filename)
  file_path = os.path.dirname(outpath)
  print("Create " + outpath)
  
  # ディレクトリが存在しなければ生成
  if not os.path.exists(file_path):
    os.makedirs(file_path)

  plt.savefig(outpath)
  plt.gcf().clear()

def init(title, xlabel, ylabel):
  # general config
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)

# データを散布図でプロットする
def plot_data(x, y, s=1):
  ## sはドットの太さ。markerでドット文字を変更できる
  plt.scatter(x, y, s=s)

# テストデータのbiasをプロットする
def plot_bias(x, func :str):
  f_type = test_data.bias_type()
  if not func in f_type:
    raise "%s no exist" % func

  plt.plot(x, eval("test_data.%s_bias(x)" % func), "g--")
