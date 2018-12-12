# coding: UTF-8
import numpy as np
from scipy.optimize import curve_fit

# 1次関数
def liner_func(x, a, b):
  return a*x + b

# 指数関数
def exp_func(x, a, b):
  return a*pow(b,x)

# べき関数
def pow_func(x,a,b):
  return a*pow(x,b)

class Scipy:
  # ax+bでのa,bを返す
  @classmethod
  def fit(cls, x, y):
    parameter_initial = np.array([0.0, 0.0]) #a, b,
    paramater_optimal, _ = curve_fit(liner_func, x, y, p0=parameter_initial)
    return paramater_optimal[0], paramater_optimal[1]

class Numpy:
  # ax+bのa,bを返す
  @classmethod
  def fit(cls, x, y):
    X = np.vstack([x, np.ones(len(x))]).T
    a, b = np.linalg.lstsq(X,y,rcond=None)[0]
    return a, b

class Original:
  # ax+bのa,bを返す
  @classmethod
  def fit(cls, x, y):
    x_sum = y_sum = xx_sum = yy_sum = xy_sum = 0.
    for i in range(x.size):
      x_sum = x_sum + x[i]
      xx_sum = xx_sum + x[i]**2
      y_sum = y_sum + y[i]
      yy_sum = yy_sum + y[i]**2
      xy_sum = xy_sum + x[i]*y[i]
    delta = x.size*xx_sum - x_sum**2
    a = (x.size*xy_sum - x_sum*y_sum)/delta
    b = (xx_sum*y_sum - x_sum*xy_sum)/delta
    return a, b
  
