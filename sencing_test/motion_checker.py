#!/usr/bin/python
# -*- coding: utf-8 -*-
import smbus            # use I2C
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
train_data_set_ax = pd.read_csv('pick/pick_accel_x.csv', usecols=[2]).values.reshape(-1, 1)
train_data_set_ay = pd.read_csv('pick/pick_accel_y.csv', usecols=[0]).values.reshape(-1, 1)
train_data_set_az = pd.read_csv('pick/pick_accel_z.csv', usecols=[2]).values.reshape(-1, 1)
train_data_set_gx = pd.read_csv('pick/pick_gyro_x.csv', usecols=[0]).values.reshape(-1, 1)
train_data_set_gy = pd.read_csv('pick/pick_gyro_y.csv', usecols=[0]).values.reshape(-1, 1)
train_data_set_gz = pd.read_csv('pick/pick_gyro_z.csv', usecols=[0]).values.reshape(-1, 1)

# Dropの学習用データを定義
drop_train_data_set_ax = pd.read_csv('drop/drop_accel_x.csv', usecols=[0]).values.reshape(-1, 1)
drop_train_data_set_ay = pd.read_csv('drop/drop_accel_y.csv', usecols=[0]).values.reshape(-1, 1)
drop_train_data_set_az = pd.read_csv('drop/drop_accel_z.csv', usecols=[0]).values.reshape(-1, 1)
drop_train_data_set_gx = pd.read_csv('drop/drop_gyro_x.csv', usecols=[0]).values.reshape(-1, 1)
drop_train_data_set_gy = pd.read_csv('drop/drop_gyro_y.csv', usecols=[0]).values.reshape(-1, 1)
drop_train_data_set_gz = pd.read_csv('drop/drop_gyro_z.csv', usecols=[0]).values.reshape(-1, 1)

# 左ワイパースイング学習データ
waiper_left_data_set_ax = pd.read_csv('waiper_left/waiper_left_accel_x.csv', usecols=[0]).values.reshape(-1, 1)
waiper_left_data_set_ay = pd.read_csv('waiper_left/waiper_left_accel_y.csv', usecols=[0]).values.reshape(-1, 1)
waiper_left_data_set_gz = pd.read_csv('waiper_left/waiper_left_gyro_z.csv', usecols=[0]).values.reshape(-1, 1)

# 右ワイパースイング学習データ
waiper_right_data_set_ax = pd.read_csv('waiper_right/waiper_right_accel_x.csv', usecols=[0]).values.reshape(-1, 1)
waiper_right_data_set_ay = pd.read_csv('waiper_right/waiper_right_accel_y.csv', usecols=[0]).values.reshape(-1, 1)
waiper_right_data_set_gz = pd.read_csv('waiper_right/waiper_right_gyro_z.csv', usecols=[0]).values.reshape(-1, 1)


# 手を下に下げる動作の学習データ
hand_down_data_set_ay = pd.read_csv('hand_down/hand_down_accel_ay.csv', usecols=[0]).values.reshape(-1, 1)
hand_down_data_set_az = pd.read_csv('hand_down/hand_down_accel_az.csv', usecols=[0]).values.reshape(-1, 1)
hand_down_data_set_gx = pd.read_csv('hand_down/hand_down_gyro_x.csv', usecols=[0]).values.reshape(-1, 1)

# 手を上にあげる動作の学習データ
hand_up_data_set_ay = pd.read_csv('hand_up/hand_up_accel_ay.csv', usecols=[0]).values.reshape(-1, 1)
hand_up_data_set_az = pd.read_csv('hand_up/hand_up_accel_az.csv', usecols=[0]).values.reshape(-1, 1)
hand_up_data_set_gx = pd.read_csv('hand_up/hand_up_gyro_x.csv', usecols=[0]).values.reshape(-1, 1)

# テストデータを作成するための初期データを作成
test_data_set_ax = np.arange(50, dtype=float).reshape(-1, 1)
test_data_set_ay = np.arange(50, dtype=float).reshape(-1, 1)
test_data_set_az = np.arange(50, dtype=float).reshape(-1, 1)
test_data_set_gx = np.arange(50, dtype=float).reshape(-1, 1)
test_data_set_gy = np.arange(50, dtype=float).reshape(-1, 1)
test_data_set_gz = np.arange(50, dtype=float).reshape(-1, 1)

pick_dtw_gx_list = []
pick_dtw_gy_list = []
drop_dtw_gx_list = []
drop_dtw_gy_list = []


pick_dtw_gx_result = []
pick_dtw_gx_result_1 = []
pick_dtw_gx_result_2 = []
pick_dtw_gx_result_3 = []
pick_dtw_gx_result_4 = []

pick_dtw_gy_result = []
pick_dtw_gy_result_1 = []
pick_dtw_gy_result_2 = []
pick_dtw_gy_result_3 = []
pick_dtw_gy_result_4 = []
"""
データ数120個の枠内に新しいデータを挿入し不要なデータをドロップさせる
* 枠内のデータ数は考える必要あり

@param 観測データセット
@param 観測データ

@return 生成した観測データセット
"""
def remake_test_data_set(test_data_set, data):
    new_data = np.insert(test_data_set, 50, data ,axis=0)
    new_data = np.delete(new_data, 0, 0)
    return new_data

# 1byte read
def read_byte( addr ):
    return bus.read_byte_data( DEV_ADDR, addr )
 
# 2byte read
def read_word( addr ):
    high = read_byte( addr   )
    low  = read_byte( addr+1 )
    return (high << 8) + low
 
# Sensor data read
def read_word_sensor( addr ):
    val = read_word( addr )
    if( val < 0x8000 ):
        return val # positive value
    else:
        return val - 65536 # negative value
 
# Get Temperature
def get_temp():
    temp = read_word_sensor( TEMP_OUT )
    # offset = -521 @ 35℃
    return ( temp + 521 ) / 340.0 + 35.0
 
# Get Gyro data (raw value)
def get_gyro_data_lsb():
    x = read_word_sensor( GYRO_XOUT )
    y = read_word_sensor( GYRO_YOUT )
    z = read_word_sensor( GYRO_ZOUT )
    return [ x, y, z ]
# Get Gyro data (deg/s)
def get_gyro_data_deg():
    x,y,z = get_gyro_data_lsb()
    # Sensitivity = 131 LSB/(deg/s), @cf datasheet
    x = x / 131.0
    y = y / 131.0
    z = z / 131.0
    return [ x, y, z ]
 
# Get Axel data (raw value)
def get_accel_data_lsb():
    x = read_word_sensor( ACCEL_XOUT )
    y = read_word_sensor( ACCEL_YOUT )
    z = read_word_sensor( ACCEL_ZOUT )
    return [ x, y, z ]
# Get Axel data (G)
def get_accel_data_g():
    x,y,z = get_accel_data_lsb()
    # Sensitivity = 16384 LSB/G, @cf datasheet
    x = x / 16384.0
    y = y / 16384.0
    z = z / 16384.0
    return [x, y, z]

def insert_csv(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z):
    with open('sample.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow([gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z])
### Main function ######################################################
bus = smbus.SMBus( 1 )
bus.write_byte_data( DEV_ADDR, PWR_MGMT_1, 0 )

"""
pick動作を検出する

@param 加速度、各加速度を用いたDTWの値
"""
def check_pick_motion(dtw_ax_result, dtw_ay_result, dtw_az_result, dtw_gx_result, dtw_gy_result):
    if 0.75 < accel_z and dtw_gx_result < 500:
        print ('pick')
        return 'pick'


"""
決定木第一段階
Ｘ軸 ＝ 0.98 → なし
Ｘ軸 = -0.98 → なし
Y軸 = 0.98 → wiper right, wiper left 
Y軸 = -0.98 → なし
Z軸 = 0.98 → pick, drop, hand down 
Z軸 = -0.98 → hand up
ジェスチャ可能性なし
"""
def check_motion_first_level(ax, ay, az):
    if 0.75 < ay < 1.25:
        return "waiper gesture"
    elif 0.75 < az < 1.25:
        return "pick drop down gesture"
    elif - 1.25 < az < -0.75:
        return "hand up gesture"
    else:
        return "not gesture"

"""
DTW間の差分を取り動作を出力する
"""
def operation_identification(diff_ax, diff_gx, diff_gy, ay, az):
    print(diff_ax, diff_gx, diff_gy, ay, az)
    if diff_ax > 20 and diff_gx > 2000 and diff_gy > -350 and 0.75 < az < 1.25:
        return 'pick'
    elif diff_ax < -15 and diff_gx < -2000 and diff_gy < -300 and 0.65 < az < 1.25:
        return 'drop'

"""
Drop動作を検出する
@param 加速度、各加速度を用いたDTWの値
"""
def check_drop_motion(drop_dtw_ax_result, drop_dtw_ay_result, drop_dtw_az_result, drop_dtw_gx_result, drop_dtw_gy_result):
    if 0.75 < accel_z and  drop_dtw_gx_result < 500:
        print('drop')
        return 'drop'
"""
観測データを出力する
"""
def print_sencing_data():
    temp = get_temp()
    print 't= %.2f' % temp, '\t',

    gyro_x,gyro_y,gyro_z = get_gyro_data_deg()
    print 'Gx= %.3f' % gyro_x, '\t',
    print 'Gy= %.3f' % gyro_y, '\t',
    print 'Gz= %.3f' % gyro_z, '\t',

    accel_x,accel_y,accel_z = get_accel_data_g()
    print 'Ax= %.3f' % accel_x, '\t',
    print 'Ay= %.3f' % accel_y, '\t',
    print 'Az= %.3f' % accel_z, '\t',
    print # 改行

def print_pick_dtw_result(ax, ay, az, gx, gy):
    print('-----------------------pick dtw result-------------------------------')
    print(ax)
    print(ay)
    print(az)
    print(gx)
    print(gy)
    print('--------------------------------end-----------------------------------')

def print_drop_dtw_result(ax, ay, az, gx, gy):
    print('-----------------------drop dtw result--------------------------------')
    print(ax)
    print(ay)
    print(az)
    print(gx)
    print(gy)
    print('--------------------------------end------------------------------------')

def check_pick_or_drop(pick_diw_x, pick_dtw_y, drop_dtw_x, drop_dtw_y):
    print(pick_diw_x)
    if pick_diw_x < drop_dtw_x and pick_dtw_y < drop_dtw_y:
        return 'pick'
    elif pick_diw_x > drop_dtw_x and pick_dtw_y > drop_dtw_y:
        return 'drop'
def get_min_data(dtw_1, dtw_2, dtw_3, dtw_4, dtw_5):
    gx_list = []
    gx_list.append(min(dtw_1))
    gx_list.append(min(dtw_2))
    gx_list.append(min(dtw_3))
    gx_list.append(min(dtw_4))
    gx_list.append(min(dtw_5))
    return min(gx_list)

count = 0
drop_count = 0
tt = 0
while 1:
    sec = time.time()
    # print_sencing_data()
    # print 'csvファイル書き込み'
    # insert_csv(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)

    # 加速度を取得
    accel_x, accel_y, accel_z = get_accel_data_g()
    # 角加速度を取得
    gyro_x, gyro_y, gyro_z = get_gyro_data_deg()
    
    # 枠内にデータを作成する
    test_data_set_ax = remake_test_data_set(test_data_set_ax, accel_x)
    test_data_set_ay = remake_test_data_set(test_data_set_ay, accel_y)
    test_data_set_az = remake_test_data_set(test_data_set_az, accel_z)
    test_data_set_gx = remake_test_data_set(test_data_set_gx, gyro_x)
    test_data_set_gy = remake_test_data_set(test_data_set_gy, gyro_y)
    test_data_set_gz = remake_test_data_set(test_data_set_gz, gyro_z)

    if 0.6 < accel_z < 1.25:
        print("--------------------------------------pick ax ay gz----------------------------------------------")
        print(dtw.getDTW(train_data_set_ax, test_data_set_ax))
        print(dtw.getDTW(train_data_set_ay, test_data_set_ay))
        print(dtw.getDTW(train_data_set_gz, test_data_set_gz))
        print("--------------------------------------drop ax ay gz----------------------------------------------")
        print(dtw.getDTW(drop_train_data_set_ax, test_data_set_ax)) 
        print(dtw.getDTW(drop_train_data_set_ay, test_data_set_ay))
        print(dtw.getDTW(drop_train_data_set_gz, test_data_set_gz))
        print("---------------------------------------hand down ay az gx----------------------------------------")
        print(dtw.getDTW(hand_down_data_set_ay, test_data_set_ay))
        print(dtw.getDTW(hand_down_data_set_az, test_data_set_az))
        print(dtw.getDTW(hand_down_data_set_gx, test_data_set_gx))
    elif -0.3 < accel_z < 0.3:
        print("----------------------------------------waiper left ax ay gz--------------------------------------")
        print(dtw.getDTW(waiper_left_data_set_ay, test_data_set_ay))
        print(dtw.getDTW(waiper_left_data_set_ax, test_data_set_ax))
        print(dtw.getDTW(waiper_left_data_set_gz, test_data_set_gz))
        print("----------------------------------------waiper right ax ay gz----------------------------------")
        print(dtw.getDTW(waiper_right_data_set_ax, test_data_set_ax))
        print(dtw.getDTW(waiper_right_data_set_ay, test_data_set_ay))
        print(dtw.getDTW(waiper_right_data_set_gz, test_data_set_gz))
    elif -1.25 < accel_z < -0.6:
        print("-------------------------------------hand up ay az gx----------------------------------------------")
        print(dtw.getDTW(hand_up_data_set_ay, test_data_set_ay))
        print(dtw.getDTW(hand_up_data_set_az, test_data_set_az))
        print(dtw.getDTW(hand_up_data_set_gx, test_data_set_gx))
    else:
        print("動作なし")
    """ 
    if tt > 80 and check_motion_first_level(accel_x, accel_y, accel_z) == "waiper gesture":    
        waiper_left_dtw_ax_result = dtw.getDTW(waiper_left_data_set_ax, test_data_set_ax)
        waiper_left_dtw_gy_result = dtw.getDTW(waiper_left_data_set_gy, test_data_set_gy)
    
        # axに着いてはDTWの値を使用してgyｙに着いてはDTWの差分を利用してデータを取得する
        waiper_right_dtw_ax_result = dtw.getDTW(waiper_right_data_set_ax, test_data_set_ax)
        waiper_right_dtw_gy_result = dtw.getDTW(waiper_right_data_set_gy, test_data_set_gy)
        # if accel_x < -0.98:
        #     print("waiper right")
        # elif accel_x > 0.98:
        #     print("waiper left")

        print("====================waiper left dtw====================================")
        print(waiper_left_dtw_ax_result)
        print(waiper_left_dtw_gy_result)
        print("====================waiper right dtw====================================")
        print(waiper_right_dtw_ax_result)
        print(waiper_right_dtw_gy_result)

    elif check_motion_first_level(accel_x, accel_y, accel_z) == "pick drop down gesture":
        pick_dtw_ax_result = dtw.getDTW(train_data_set_ax, test_data_set_ax)
        pick_dtw_ay_result = dtw.getDTW(train_data_set_ay, test_data_set_ay)
        pick_dtw_gx_result = dtw.getDTW(train_data_set_gx, test_data_set_gx)
        pick_dtw_gy_result = dtw.getDTW(train_data_set_gy, test_data_set_gy)
        drop_dtw_ax_result = dtw.getDTW(drop_train_data_set_ax, test_data_set_ax)
        drop_dtw_gx_result = dtw.getDTW(drop_train_data_set_gx, test_data_set_gx)
        drop_dtw_gy_result = dtw.getDTW(drop_train_data_set_gy, test_data_set_gy)
    # if accel_z > 1:
    #     print("hand down gesture")
    # elif operation_identification(drop_dtw_ax_result - pick_dtw_ax_result, drop_dtw_gx_result - pick_dtw_gx_result, drop_dtw_gy_result - pick_dtw_gy_result, accel_y, accel_z) == 'drop':
    #     print("drop")
    # elif operation_identification(drop_dtw_ax_result - pick_dtw_ax_result, drop_dtw_gx_result - pick_dtw_gx_result, drop_dtw_gy_result - pick_dtw_gy_result, accel_y, accel_z) == 'pick':
    #     print("pick")
    # pickとdropはDTWの差分を使用して分類する
    

        # ax ay の値がhand downに近づけば無条件でhand downを検出する
        hand_down_dtw_ay_result = dtw.getDTW(hand_down_data_set_ay, test_data_set_ay)
        hand_down_dtw_az_result = dtw.getDTW(hand_down_data_set_az, test_data_set_az)
        print("====================pick dtw====================================")
        print(pick_dtw_ax_result)
        print(pick_dtw_ay_result)
        print(pick_dtw_gx_result)
        print(pick_dtw_gy_result)
        print("====================drop dtw====================================")
        print(drop_dtw_ax_result)
        print(drop_dtw_gx_result)
        print(drop_dtw_gy_result)

        print("====================hand down dtw====================================")
        print(hand_down_dtw_ay_result)
        print(hand_down_dtw_az_result)
    elif check_motion_first_level(accel_x, accel_y, accel_z) == "hand up gesture":
        # ax, ayのDTWの値に直接閾値を用いる
        hand_up_dtw_ay_result = dtw.getDTW(hand_up_data_set_ay, test_data_set_ay)
        hand_up_dtw_az_result = dtw.getDTW(hand_up_data_set_az, test_data_set_az)
        print("====================hand up dtw====================================")
        print(hand_up_dtw_ay_result)
        print(hand_up_dtw_az_result)
    # if accel_x < -1.2:
    #     print("hand down gesture")
    else:
        print("not gesture")
    """
    pick_dtw_gx_list = []
    pick_dtw_gy_list = []
    drop_dtw_gx_list = []
    drop_dtw_gy_list = []
    tt += 1
    elapsed_time = time.time()
    print(elapsed_time - sec)
