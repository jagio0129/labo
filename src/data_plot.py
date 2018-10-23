# coding: UTF-8

import configparser
import os
import time
import numpy as np
import matplotlib
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt
import pandas as pd

from lib import utils

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH = c["GRAVITY_PATH"]
GRAVITY_IMAGE_PATH = GRAVITY_PATH + "/img"

# 人口を１万で割る
def optimize(pop):
  return round(pop / 10000, 3)

### main
if __name__ == '__main__':
  start = time.time()
  utils.dump_description("Plot Gravity Model data.")

  # ODデータファイルに対し以下の処理
  for abs_file in utils.file_list(GRAVITY_PATH):
    print("Load: " + abs_file)

    # csv load
    df = pd.read_csv(abs_file)
    origin_pop  = list(map(optimize, df["origin_pop"].values))
    dest_pop    = list(map(optimize, df["dest_pop"].values))
    distance    = df["distance"].values
    amount      = df['amount'].values
    r           = df['right_fomula'].values
    
    # figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # 散布図 config
    ## sはドットの太さ。markerでドット文字を変更できる
    ax.scatter(amount, r, s=1)
       
    # general config
    ax.set_title('Gravity Model')
    ax.set_xlabel('Amount')
    ax.set_ylabel('Right fomula')
    plt.xlim([0,50])  # x range
    plt.ylim([0,400])  # y range
      
    # save as png
    date_name = utils.file_date(abs_file)
    tags = "/x50y400"
    outpath = GRAVITY_IMAGE_PATH + tags + "/figure-" + date_name + ".png"
    print("Create " + outpath)
    plt.savefig(outpath)

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
