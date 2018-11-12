# coding: UTF-8

import matplotlib
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
import os

def export(path, dir, tag, filename):
  outpath = "%s/%s/%s/%s.png" % (path, dir, tag, filename) 
  file_path = os.path.dirname(outpath)
  print("Create " + outpath)
  
  # ディレクトリが存在しなければ生成
  if not os.path.exists(file_path):
    os.makedirs(file_path)

  plt.savefig(outpath)

# matplotlib 初期化
def plot(xvalues, yvalues, title, xlabel, ylabel):
  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)

  # 散布図 config
  ## sはドットの太さ。markerでドット文字を変更できる
  ax.scatter(xvalues, yvalues, s=1)
    
  # general config
  ax.set_title(title)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)

# 片対数
def single_log_plot(xvalues, yvalues, title, xlabel, ylabel):
  plot(xvalues, yvalues, title, xlabel, ylabel)
  # log
  plt.xscale("log")

# 両対数
def multi_log_plot(xvalues, yvalues, title, xlabel, ylabel):
  plot(xvalues, yvalues, title, xlabel, ylabel)
  # log
  plt.xscale("log")
  plt.yscale("log")
