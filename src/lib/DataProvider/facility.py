# coding: UTF-8
import pandas as pd
from collections import defaultdict

# 施設一覧
def facility_list(data_frame):
  return data_frame['type1'].unique()


