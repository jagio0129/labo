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

### main
if __name__ == '__main__':
  start = time.time()
  utils.dump_description("Plot Gravity Model data.")

  # ODデータファイルに対し以下の処理
  for abs_file in utils.file_list(GRAVITY_PATH):
    print("Load: " + abs_file)

    # csv load
    df = pd.read_csv(abs_file)
    devided_data  = df["devided"].values
    devide_data   = df["devide"].values
    gravity_data  = df["gravity_parameter"].values
    
    # figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # 散布図 config
    ## sはドットの太さ。markerでドット文字を変更できる
    ax.scatter(devided_data, devide_data, s=1)
       
    # general config
    ax.set_title('Parameter G of Gravity Model')
    ax.set_xlabel('amountAB × distAB')
    ax.set_ylabel('popA × popB')
    plt.xlim([0,200])  # x range
    plt.ylim([0,2000])  # y range
      
    # save as png
    date_name = utils.file_date(abs_file)
    tags = "/x200y2000"
    outpath = GRAVITY_IMAGE_PATH + tags + "/figure-" + date_name + ".png"
    print("Create " + outpath)
    plt.savefig(outpath)

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
