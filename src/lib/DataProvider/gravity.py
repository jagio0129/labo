# coding: UTF-8
from math import sin, cos, acos, radians

earth_rad = 6378.137

# 緯度経度をxyz座標系に変換
def __latlng_to_xyz(lat, lng):
  rlat, rlng = radians(lat), radians(lng)
  coslat = cos(rlat)
  return coslat*cos(rlng), coslat*sin(rlng), sin(rlat)

# ２点間の距離[km]をを返す
## return float
def dist_on_sphere(pos0, pos1, radious=earth_rad):
  xyz0, xyz1 = __latlng_to_xyz(*pos0), __latlng_to_xyz(*pos1)
  return acos(sum(x * y for x, y in zip(xyz0, xyz1)))*radious

# グラビティモデルの式
## popA, popB = 人口、 distAB = AB間の距離
def fomula(popA, popB, distAB):
  g = 1   # 何かしらのパラメータ
  f = g * (popA * popB) / distAB

