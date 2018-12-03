# coding: UTF-8

import matplotlib
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import os

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

# 1次関数
def liner_func(x, a, b):
  return a*x + b

# 指数関数
def exp_func(x, a, b):
  return np.exp(a*x) + b

# べき関数
def pow_func(x,a,b):
  return a*pow(x,b)

def fit(xdata, ydata, func):
  parameter_initial = np.array([0.0, 0.0]) #a, b,
  paramater_optimal, _ = curve_fit(func, xdata, ydata, p0=parameter_initial)
  y = func(xdata,paramater_optimal[0],paramater_optimal[1])
  plt.plot(xdata, y, '-', color='red')

# 直線フィッティング
def liner_fit(xdata, ydata):
  fit(xdata, ydata, liner_func)

# 指数関数フィッティング
def exp_fit(xdata, ydata):
  fit(xdata, ydata, exp_func)

# べき関数フィッティング
def pow_fit(xdata, ydata):
  fit(xdata, ydata, pow_func)

class Numpy():

  # 最小二乗法で係数a,bを取得
  @classmethod
  def _lstsq(self, x, y):
    A = np.array([x,np.ones(len(x))])
    A = A.T
    a, b = np.linalg._lstsq(A,y,rcond=-1)[0]
    return a, b

  
  @classmethod
  def liner_fit(cls, x, y):
    a, b = cls._lstsq(x, y)
    plt.plot(x,liner_func(x, a, b), "r--")

  @classmethod
  def exp_fit(cls, x, y):
    a, b = cls._lstsq(x, y)
    plt.plot(x,exp_func(x, a, b), "r--")
  
  @classmethod
  def pow_fit(cls, x, y):
    a, b = cls._lstsq(x, y)
    plt.plot(x,pow_func(x, a, b), "r--")