# coding: UTF-8
from math import sin, cos, acos, radians
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

earth_rad = 6378.137

# 緯度経度をxyz座標系に変換
def __latlng_to_xyz(lat, lng):
  rlat, rlng = radians(lat), radians(lng)
  coslat = cos(rlat)
  return coslat*cos(rlng), coslat*sin(rlng), sin(rlat)

# ２点間の距離[km]をを返す
## return float
def dist_on_sphere(pos0, pos1, radious=earth_rad):
  if (str(None) in pos0) or (str(None) in pos1):
    return None
  xyz0, xyz1 = __latlng_to_xyz(*pos0), __latlng_to_xyz(*pos1)
  return acos(sum(x * y for x, y in zip(xyz0, xyz1)))*radious

# グラビティモデルによる移動量の算出
## popA, popB = 人口、 distAB = AB間の距離
def fomula(popA, popB, distAB):
  g = 1   # 何かしらのパラメータ
  f = g * ((popA * popB) / distAB)

  return f

# グラビティモデルのパラメータGを算出する
#   args
#     amount = 移動量, popA, popB = 人口, distAB = ２点間距離
#   return
#     devided = 移動量, devide = 人口×距離, g = パラメータ,
def param_fomuola(amount, popA, popB, distAB):
  if((amount is None) or (popA is None) or (popB is None) or (distAB is None)):
    dump_params(amount, None, popA, None, popB, distAB)
    raise
  if((amount == 0) or (popA == 0) or (popB ==0) or (distAB == 0)):
    dump_params(amount, None, popA, None, popB, distAB)
    raise

  popA = round(popA/10000, 3)  # 1万で割り、有効数字３桁に丸める
  popB = round(popB/10000, 3)  # 1万で割り、有効数字３桁に丸める
  
  devided   = float(amount) * float(distAB)
  devide    = float(popA) * float(popB)
  g = devided / devide
  g = round(g,3)

  return devided, devide, g

# cityIDの人口を取得する
def population(population_data, city_id):
  if city_id == str(None):
    return None

  # 人口データをロード
  df = pd.read_csv(population_data)

  for index, row in df.iterrows():
    if int(city_id) == int(row["city_id"]):
      return row["population"]
  return None

# 各パラメータの値を表示する。
def dump_params(amount=None, origin=None, popA=None, destination=None, popB=None, distAB=None):
  print("Origin: %s , 人口: %s 人" % (origin, popA))
  print("Destination: %s , 人口: %s 人" % (destination, popB))
  print("2点間の距離: %s km" % distAB)
  print("2点間の移動量: %s 人" % amount)

