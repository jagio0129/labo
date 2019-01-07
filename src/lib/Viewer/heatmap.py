# coding: UTF-8

import os
import pandas as pd
import matplotlib
matplotlib.rcParams['font.family'] = 'IPAexGothic'
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
import matplotlib.font_manager
import matplotlib.cm as cm
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
# フォントのデータのパス
# print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
# フォントの指定名確認
# print([f.name for f in matplotlib.font_manager.fontManager.ttflist])  

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

def plot_heatmap(data_frame,values,column,index):
  unq_x, unq_y = len(data_frame.origin.unique()), len(data_frame.destination.unique())
  print("Destination : %d, Origin : %d" % (unq_x, unq_y))

  # plotするデータの整形
  df_pivot = pd.pivot_table(data=data_frame, values=values, columns=column, index=index)

  ratio = 8
  fig = plt.figure(figsize=(len(df_pivot.columns)/ratio, len(df_pivot)/ratio),dpi=100) #...1

  plt.title("Heat Map",fontsize=40)
  plt.xlabel("Destination",fontsize=30)
  plt.ylabel("Origin", fontsize=30)

  # 列ごとに値の降順ソート
  for column in df_pivot.columns.values:
    df_pivot = df_pivot.sort_values(by=column,ascending=False)
  print(df_pivot)
  
  plt.yticks(fontsize=3)              # y軸のlabel
  plt.xticks(rotation=90,fontsize=3) # x軸のlabel
  
  # cbarの設定
  cmap = sns.cubehelix_palette(as_cmap=True, light=.9)
  # null値をマスクして表示するための設定。
  mask = df_pivot.isnull()

  ax = sns.heatmap(df_pivot, cbar_kws={'label': 'Amount'}, cmap='OrRd', mask=mask)
  ax.set_facecolor('#3cb371') # null値の色を設定
  ax.figure.axes[-1].yaxis.label.set_size(30) # cbarのラベルのサイズ
