# coding: UTF-8

# ユーザ一覧
def list(data_frame):
  return data_frame['user_id'].unique()

# 存在しないuser_idの一覧を表示する
def not_exist(user_list):
  user_list.sort()
  i = 0
  num = []
  for id in user_list:
    if not (i in user_list):
      while (i != int(id)):
        num.append(i)
        i = i + 1
    i = i + 1
  print("No exist UserID:")
  print(num)
  print("Size: %d" % len(num))