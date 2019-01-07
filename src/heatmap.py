# coding: UTF-8
import time
import os
import configparser
import pandas as pd
import numpy as np

from lib import utils
from lib.Viewer import ploter
from lib.Viewer import heatmap
from lib.DataProvider import test_data

SOURCE_PATH = os.path.dirname(os.path.abspath(__file__))

c = configparser.ConfigParser()
c.read(SOURCE_PATH + '/config.ini')
c = c["DEFAULT"]

GRAVITY_PATH     = c["GRAVITY_PATH"] + "/default"
TEST_DATA   = [GRAVITY_PATH + "/gravity_param-od-2013-07-01.csv"]

def main(gravity_path, a4d4_f, tags):
  # for abs_file in utils.file_list(gravity_path): # 実データ用
  for abs_file in TEST_DATA:  # テスト用
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
    
    heatmap.plot_heatmap(df, 'amount', 'origin', 'destination')
    # plot_heatmap(dest,origin,amount)

    date_name = utils.file_date(abs_file)
    outpath = c["DATA_PATH"] + "/gravity_heatmap" + tags
    #ploter.export(outpath, date_name)
    heatmap.export_pdf(outpath,date_name)

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
  # a4d4()
  # one_point()
  # onepoint_a4d4()

  elapsed_time = time.time() - start
  print("elapsed_time:{0}".format(elapsed_time) + "[sec]")