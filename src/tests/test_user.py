# coding: UTF-8
import unittest
import sys
import os
import pandas as pd
sys.path.append("../")

from lib.DataProvider import user

ROOT_PATH = "/home/vagrant/mount_folder/repo/person_trip"
DATA_PATH = os.path.join(ROOT_PATH, "data")
PERSON_TRIP = os.path.join(DATA_PATH, "person_trip")
TEST_CSV = os.path.join(PERSON_TRIP, "2013-07-01.csv")

data_frame = pd.read_csv(TEST_CSV)

class UserTest(unittest.TestCase):

  def test_not_exist(self):
    not_users, user_number = user.not_exist(data_frame)
