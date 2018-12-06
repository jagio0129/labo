# coding: UTF-8

import matplotlib
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import os
import math
from lib.DataProvider import mymath 

def export(path, filename="default"):
  outpath = "%s/%s.png" % (path, filename)
  file_path = os.path.dirname(outpath)
  print("Create " + outpath)
  
  # ディレクトリが存在しなければ生成
  if not os.path.exists(file_path):
    os.makedirs(file_path)

  plt.savefig(outpath)
  plt.gcf().clear()

# matplotlib 初期化
def plot(xvalues, yvalues, title, xlabel, ylabel):
  # general config
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)

  # 散布図 config
  ## sはドットの太さ。markerでドット文字を変更できる
  plt.scatter(xvalues, yvalues, s=1)

# 片対数
def single_log_plot(xvalues, yvalues, title, xlabel, ylabel):
  plot(xvalues, yvalues, title, xlabel, ylabel)
  # log
  plt.yscale("log")

# 両対数
def multi_log_plot(xvalues, yvalues, title, xlabel, ylabel):
  plot(xvalues, yvalues, title, xlabel, ylabel)
  # log
  plt.xscale("log")
  plt.yscale("log")

class Scipy():

  @classmethod
  def fit(cls, xdata, ydata, func):
    parameter_initial = np.array([0.0, 0.0]) #a, b,
    paramater_optimal, _ = curve_fit(func, xdata, ydata, p0=parameter_initial)
    y = func(xdata,paramater_optimal[0],paramater_optimal[1])
    plt.plot(xdata, y, '-', color='red')

  @classmethod
  # 直線フィッティング
  def liner_fit(cls, xdata, ydata):
    cls.fit(xdata, ydata, mymath.liner_func)

  @classmethod
  # 指数関数フィッティング
  def exp_fit(cls, xdata, ydata):
    cls.fit(xdata, ydata, mymath.exp_func)

  @classmethod
  # べき関数フィッティング
  def pow_fit(cls, xdata, ydata):
    cls.fit(xdata, ydata, mymath.pow_func)

class Numpy():

  @classmethod
  def liner_fit(cls, x, y):
    X = np.vstack([x, np.ones(len(x))]).T
    a,b = np.linalg.lstsq(X,y,rcond=None)[0]
    plt.plot(x,mymath.liner_func(x, a, b), "r-")

  @classmethod
  def exp_fit(cls, x, y):
    # 片対数を取ることで線形化
    logy = np.log(y)
    X = np.vstack([x, np.ones(len(x))]).T
    b,a = np.linalg.lstsq(X,logy,rcond=None)[0]
    a = math.e ** a
    b = math.e ** b
    plt.plot(x,mymath.exp_func(x, a, b), "r-")
  
  @classmethod
  def pow_fit(cls, x, y):
    # 両対数を取ることで線形化
    logx, logy = np.log(x), np.log(y)
    X = np.vstack([logx, np.ones(len(logx))]).T
    b,a = np.linalg.lstsq(X,logy,rcond=None)[0]
    a = math.e ** a
    plt.plot(x,mymath.pow_func(x, a, b), "r-")