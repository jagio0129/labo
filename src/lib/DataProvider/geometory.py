# coding: UTF-8

import jpgrid
from tqdm import tqdm

# 緯度経度からメッシュコードに換算しdfに追加して返す(1次=4桁、2次=6桁、3次=8桁)
## return data_frame
def add_meshcode_column(data_frame):
  print("  Calculating mesh code...")
  pbar = tqdm(total=len(data_frame))  # for progress bar
  for index, row in data_frame.iterrows():
    mc3 = jpgrid.encodeLv3(row["latitude"], row["longitude"])
    data_frame.at[index, "mesh_code_lv1"] = mc3[:4]
    data_frame.at[index, "mesh_code_lv2"] = mc3[:6]
    data_frame.at[index, "mesh_code_lv3"] = mc3
    pbar.update(1)

  pbar.close()
  return data_frame

# 各メッシュコードのユーザがどのくらいいるかチェック
def mesh_counter(data_frame, time_range, lv):
  if (lv == 1 or lv == 2 or lv == 3):
    mask = (data_frame['date'] >= time_range) & (data_frame['date'] < time_range+1)
    data_frame = data_frame.loc[mask]
    h = "mesh_code_lv" + str(lv)
    return data_frame[h].value_counts()
  else:
    raise "lvの値が不正"
