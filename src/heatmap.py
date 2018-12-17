# coding: UTF-8
import time
import os
import configparser
import pandas as pd
import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'IPAexGothic'
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
import matplotlib.font_manager
import matplotlib.cm as cm
from matplotlib.backends.backend_pdf import PdfPages
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

def export_pdf(path, filename="default"):
  outpath = "%s/%s.pdf" % (path, filename)
  file_path = os.path.dirname(outpath)
  print("Create " + outpath)

  # ディレクトリが存在しなければ生成
  if not os.path.exists(file_path):
    os.makedirs(file_path)

  pdf = PdfPages(outpath)
  pdf.savefig()
  pdf.close()

def plot_heatmap(x,y, value):
  unq_x, unq_y = len(np.unique(x)), len(np.unique(y))
  print("Destination : %d, Origin : %d" % (unq_x, unq_y))

  fig = plt.figure(figsize=(22, 30),dpi=100) #...1

  # Figure内にAxesを追加()
  ax = fig.add_subplot(111) #...2
  
  plt.title("Heat Map",fontsize=40)
  plt.xlabel("Destination",fontsize=30)
  plt.ylabel("Origin", fontsize=30)

  plt.yticks(fontsize=7)              # y軸のlabel
  plt.xticks(rotation=90, fontsize=14) # x軸のlabel
  color_bar(value)                    # カラーバーの表示
  plt.grid(which='major',color='gray',linestyle='--')
  plt.scatter(x, y, s=50, color=color(value))

def color_bar(value):
  m = cm.ScalarMappable(cmap=cm.jet)
  m.set_array(value)
  cbar = plt.colorbar(m)
  cbar.set_label('Amount',size=30)
  cbar.ax.tick_params(labelsize=30)
  # plt.colorbar(m).ax.tick_params(labelsize=30)

def color(value):
  return cm.jet(value/float(value.max()))

def main(gravity_path, a4d4_f, tags):
  for abs_file in utils.file_list(gravity_path): # 実データ用
  # for abs_file in TEST_DATA:  # テスト用
    print(abs_file)

    df = pd.read_csv(abs_file)
    if a4d4_f:
      df = df[(df.amount > 4) & (df.distance > 4)]
    print(df.loc[:,['origin','destination', 'amount']])
    
    origin = df.origin.values
    dest   = df.destination.values
    amount      = df.amount.values

    # テストデータ
    # origin, dest, amount = test_data.HeatMap.create()

    plot_heatmap(dest,origin,amount)

    date_name = utils.file_date(abs_file)
    outpath = c["DATA_PATH"] + "/gravity_heatmap" + tags
    #ploter.export(outpath, date_name)
    export_pdf(outpath,date_name)

def default():
  gravity_data = c["GRAVITY_PATH"] + "/default"
  a4d4_f = False
  tags = "/default"
  main(gravity_data,a4d4_f,tags)

def a4d4():
  gravity_data = c["GRAVITY_PATH"] + "/default"
  a4d4_f = True
  tags = "/a4d4"
  main(gravity_data,a4d4_f,tags)

def one_point():
  gravity_data = c["GRAVITY_PATH"] + "/one_point"
  a4d4_f = False
  tags = "/one_point"
  main(gravity_data,a4d4_f,tags)

def onepoint_a4d4():
  gravity_data = c["GRAVITY_PATH"] + "/one_point"
  a4d4_f = True
  tags = "/onepoint_a4d4"
  main(gravity_data,a4d4_f,tags)
    
if __name__ == '__main__':
  start = time.time()
  # スクリプトの概要をdump
  utils.dump_description("Plot Heat Map.")

  default()
  a4d4()
  one_point()
  onepoint_a4d4()

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")