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

# 直線フィッティング
def liner_fit(xdata, ydata):
  def func(x, a, b):
    return a*x + b
  fit(xdata,ydata,func)

# 指数関数フィッティング
def exp_fit(xdata, ydata):
  def func(x, a, b):
    return np.exp(a*x) + b
  fit(xdata,ydata,func)

# べき関数フィッティング
def pow_fit(xdata, ydata):
  def func(x, a, b):
    return pow(x,a) + b
  fit(xdata,ydata,func)

def fit(xdata, ydata, fomula):
  # initial guess for the parameters
  parameter_initial = np.array([1.0, 0.0]) #a, b
  paramater_optimal, _ = curve_fit(fomula, xdata, ydata, p0=parameter_initial)
  y = fomula(xdata,paramater_optimal[0],paramater_optimal[1])
  plt.plot(xdata, y, '-', color='red')
