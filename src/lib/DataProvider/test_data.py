# coding: UTF-8
import random
import numpy as np

# 指数関数
def exp_bias(x):
  return np.exp(x/20)

# べき関数
def pow_bias(x):
  return pow(x, 2)

# テストデータ(x,y)を生成。
#   num : 生成するデータの個数
#   bias : データを生成するのに使用する関数("exp":指数関数、"pow":べき関数)
#   margin : ランダムで誤差をつくるためのしきい値
def create(bias :str, num=50, margin=0):
  x, y = list(), list()
  for v in range(num):
    v += 1
    x.append(v)
    y.append(eval("%s_bias(v)" % bias))
  # yに誤差を発生させる
  y = [v + int(v/10) * random.randint(-margin, margin) for v in y]
  # yに対してソートする
  return np.array(x), np.array(y)
