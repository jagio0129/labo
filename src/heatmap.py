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

from lib import utils
from lib.Viewer import ploter

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH     = c["GRAVITY_PATH"] + "/default"
TEST_DATA   = [GRAVITY_PATH + "/gravity_param-od-2013-07-01.csv"]

def plot_heatmap(x,y, value):
  ploter.init(title="Heat Map", xlabel="Origin", ylabel="Destination")
  # フォントのデータのパス
  # print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
  # フォントの指定名確認
  # print([f.name for f in matplotlib.font_manager.fontManager.ttflist])
  print(value.max())
  plt.scatter(x, y, s=1, color=color(value))
  # plt.colorbar()

  outpath = "./"
  ploter.export(outpath)

def color(value):
  m = cm.ScalarMappable(cmap=cm.jet)
  m.set_array(value)
  plt.colorbar(m)
  return cm.jet(value/float(value.max()))

def main():
  # for abs_file in utils.file_list(OD_PATH): # 実データ用
  for abs_file in TEST_DATA:  # テスト用
    print(abs_file)

    df = pd.read_csv(abs_file)
    df = df[(df.amount > 4) & (df.distance > 4)]
    # for index, row in df.iterrows():
    origin = df.origin.values
    #origin = df.origin_id.values
    dest   = df.destination.values
    #dest   = df.destination_id.values
    amount      = df.amount.values

    plot_heatmap(origin,dest,amount)
    
if __name__ == '__main__':
  start = time.time()
  # スクリプトの概要をdump
  utils.dump_description("Plot Heat Map.")

  main()

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")