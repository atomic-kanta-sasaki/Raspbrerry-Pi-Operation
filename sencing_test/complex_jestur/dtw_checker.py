import math
from time import sleep  # time module
import csv
import dtw
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from matplotlib import pyplot as plt
import pandas as pd
import time

### define #############################################################
DEV_ADDR = 0x68         # device address
PWR_MGMT_1 = 0x6b       # Power Management 1
ACCEL_XOUT = 0x3b       # Axel X-axis
ACCEL_YOUT = 0x3d       # Axel Y-axis
ACCEL_ZOUT = 0x3f       # Axel Z-axis
TEMP_OUT = 0x41         # Temperature
GYRO_XOUT = 0x43        # Gyro X-axis
GYRO_YOUT = 0x45        # Gyro Y-axis
GYRO_ZOUT = 0x47        # Gyro Z-axis

# Pickの学習用データを定義
train_data_set_ax = pd.read_csv('pick_data/pick_accel_x.csv', usecols=[0]).values.reshape(-1, 1)
train_data_set_ay = pd.read_csv('pick_data/pick_accel_y.csv', usecols=[0]).values.reshape(-1, 1)
train_data_set_az = pd.read_csv('pick_data/pick_accel_z.csv', usecols=[0]).values.reshape(-1, 1)
train_data_set_gx = pd.read_csv('pick_data/pick_gyro_x.csv', usecols=[0]).values.reshape(-1, 1)
train_data_set_gy = pd.read_csv('pick_data/pick_gyro_y.csv', usecols=[0]).values.reshape(-1, 1)

# Dropの学習用データを定義
drop_train_data_set_ax = pd.read_csv('drop_data/drop_accel_x.csv', usecols=[0]).values.reshape(-1, 1)
drop_train_data_set_ay = pd.read_csv('drop_data/drop_accel_y.csv', usecols=[0]).values.reshape(-1, 1)
drop_train_data_set_az = pd.read_csv('drop_data/drop_accel_z.csv', usecols=[0]).values.reshape(-1, 1)
drop_train_data_set_gx = pd.read_csv('drop_data/drop_gyro_x.csv', usecols=[0]).values.reshape(-1, 1)
drop_train_data_set_gy = pd.read_csv('drop_data/drop_gyro_y.csv', usecols=[0]).values.reshape(-1, 1)



train_data_set_ax = pd.read_csv('pick_train_data_2/pick_accel_x.csv', usecols=[2]).values.reshape(-1, 1)
train_data_set_ay = pd.read_csv('pick_train_data_2/pick_accel_y.csv', usecols=[2]).values.reshape(-1, 1)
train_data_set_az = pd.read_csv('pick_train_data_2/pick_accel_z.csv', usecols=[2]).values.reshape(-1, 1)
train_data_set_gx = pd.read_csv('pick_train_data_2/pick_gyro_x.csv', usecols=[2]).values.reshape(-1, 1)
train_data_set_gy = pd.read_csv('pick_train_data_2/pick_gyro_y.csv', usecols=[2]).values.reshape(-1, 1)

# Dropの学習用データを定義
drop_train_data_set_ax = pd.read_csv('drop_train_data/drop_accel_x.csv', usecols=[3]).values.reshape(-1, 1)
drop_train_data_set_ay = pd.read_csv('drop_train_data/drop_accel_y.csv', usecols=[3]).values.reshape(-1, 1)
drop_train_data_set_az = pd.read_csv('drop_train_data/drop_accel_z.csv', usecols=[3]).values.reshape(-1, 1)
drop_train_data_set_gx = pd.read_csv('drop_train_data/drop_gyro_x.csv', usecols=[3]).values.reshape(-1, 1)
drop_train_data_set_gy = pd.read_csv('drop_train_data/drop_gyro_y.csv', usecols=[3]).values.reshape(-1, 1)

# gx_result = dtw.getDTW(train_data_set_gx, drop_train_data_set_gx)
ax_result = dtw.getDTW(train_data_set_ax, drop_train_data_set_ax)
ay_result = dtw.getDTW(train_data_set_ay, drop_train_data_set_ay)
az_result = dtw.getDTW(train_data_set_az, drop_train_data_set_az)
gx_result = dtw.getDTW(drop_train_data_set_gx, train_data_set_gx)
gy_result = dtw.getDTW(train_data_set_gy, drop_train_data_set_gy)
print(ax_result)
print(ay_result)
print(az_result)
print(gx_result)
print(gy_result)

dtw.getDTWPath(train_data_set_gx, drop_train_data_set_gx)