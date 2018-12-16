# coding: UTF-8
import time
import os
import configparser
import pandas as pd
import matplotlib
matplotlib.rcParams['font.family'] = 'IPAexGothic'
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
import matplotlib.font_manager
import matplotlib.cm as cm
# フォントのデータのパス
# print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
# フォントの指定名確認
# print([f.name for f in matplotlib.font_manager.fontManager.ttflist])  

from lib import utils
from lib.Viewer import ploter
from lib.DataProvider import test_data

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH     = c["GRAVITY_PATH"] + "/default"
TEST_DATA   = [GRAVITY_PATH + "/gravity_param-od-2013-07-01.csv"]

def plot_heatmap(x,y, value):
  fig = plt.figure(figsize=(30, 14)) #...1

  # Figure内にAxesを追加()
  ax = fig.add_subplot(111) #...2
  
  plt.title("Heat Map",fontsize=24)
  plt.xlabel("Origin",fontsize=20)
  plt.ylabel("Destination", fontsize=20)
  plt.yticks(fontsize=18)              # y軸のlabel
  plt.xticks(rotation=90, fontsize=10) # x軸のlabel
  color_bar(value)                    # カラーバーの表示
  plt.grid(which='major',color='gray',linestyle='--')
  plt.scatter(x, y, s=100, color=color(value))

  outpath = "./"
  ploter.export(outpath)

def color_bar(value):
  m = cm.ScalarMappable(cmap=cm.jet)
  m.set_array(value)
  plt.colorbar(m).ax.tick_params(labelsize=30)

def color(value):
  return cm.jet(value/float(value.max()))

def main():
  # for abs_file in utils.file_list(OD_PATH): # 実データ用
  for abs_file in TEST_DATA:  # テスト用
    print(abs_file)

    df = pd.read_csv(abs_file)
    df = df[(df.amount > 4) & (df.distance > 4)]
    print(df.loc[:,['origin','destination', 'amount']])
    
    origin = df.origin.values
    dest   = df.destination.values
    amount      = df.amount.values

    # テストデータ
    # origin, dest, amount = test_data.HeatMap.create()

    plot_heatmap(origin,dest,amount)
    
if __name__ == '__main__':
  start = time.time()
  # スクリプトの概要をdump
  utils.dump_description("Plot Heat Map.")

  main()

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")