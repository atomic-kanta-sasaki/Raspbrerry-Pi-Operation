#!/usr/bin/python
# -*- coding: utf-8 -*-
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

# page_num = 1

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

def insert_csv(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z):
    with open('sample.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow([gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z])

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
DTW間の差分を取り動作を出力する(pick and drop)
pick dtw - drop dtw
"""
def operation_identification(diff_gz):
    print(diff_gz)
    if diff_gz < -8500:
        print("pick")
        return 'pick'
    elif diff_gz > 8500:
        print("drop")
        return 'drop'

"""
DTWの差分を取り動作を出力する waiper left
waiper_left dtw - waiper_right dtw
"""
def waiper_operation_identification(diff_gz, accel_x, latest_accel_x):
    print(diff_gz)
    print(latest_accel_x)
    if 0.7 < accel_x and -0.3 < latest_accel_x < 0.3:
        if diff_gz < -7500:
            print("waiper left")
            return "waiper left"
    if -0.7 > accel_x and -0.65 < latest_accel_x < 0.55:
        if diff_gz > 5500:
            print("waiper right")
            return "waiper right"


"""
Drop動作を検出す
@param 加速度、各加速度を用いたDTWの値
"""
def check_drop_motion(drop_dtw_ax_result, drop_dtw_ay_result, drop_dtw_az_result, drop_dtw_gx_result, drop_dtw_gy_result):
    if 0.75 < accel_z and  drop_dtw_gx_result < 500:
        print('drop')
        return 'drop'


def check_pick_or_drop(pick_diw_x, pick_dtw_y, drop_dtw_x, drop_dtw_y):
    print(pick_diw_x)
    if pick_diw_x < drop_dtw_x and pick_dtw_y < drop_dtw_y:
        return 'pick'
    elif pick_diw_x > drop_dtw_x and pick_dtw_y > drop_dtw_y:
        return 'drop'
# file_pather = 'sencing_test_result/' +page_num+ '/log_5.csv'
name_list = ['father', 'hirano', 'hiroki', 'hukukawa', 'mother', 'odaq', 'omoriku', 'sajiki', 'sasaki', 'sawayanagi', 'takagi_m1', 'tubonuma', 'watanabe_d1']
log_num = ['1', '2', '3', '4', '5']


"""
被験者のログデータをlog.csvファイルに記録する
log_(被験者名).csvファイルというファイル名に変更すること
加速度、角加速度は指標に使用しているしていないにかかわらずデータをインサートしていく
DTWの値に関しては動作分析に使用している指標のデータのみインサートしていく
pick dropやwaiperのようにDTWの差分を使用しているものが存在するため第１３引数に定義している
"""
def insert_log_data(name, num, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, ax_dtw, ay_dtw, az_dtw, gyro_x_dtw, gyro_y_dtw, gyro_z_dtw, diff_data,flag="not jestur"):
    with open('sencing_test_result/' + name + '/comparative_log_num_' + num + '.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow([accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, ax_dtw, ay_dtw, az_dtw, gyro_x_dtw, gyro_y_dtw, gyro_z_dtw, diff_data, flag])

count = 0
tt = 0
pick_count = 0
drop_count = 0
waiper_left_count = 0
waiper_right_count = 0
hand_down_count = 0
hand_up_count = 0
member_count = 0
log_count = 0

while member_count < len(name_list):

    while log_count < len(log_num):

        name_list = ['father', 'hirano', 'hiroki', 'hukukawa', 'mother', 'odaq', 'omoriku', 'sajiki', 'sasaki', 'sawayanagi', 'takagi_m1', 'tubonuma', 'watanabe_d1']
        log_num = ['1', '2', '3', '4', '5']
        log_test_data_set_ax = pd.read_csv('sencing_test_result/' + name_list[member_count] + '/log_' + log_num[log_count] + '.csv', usecols=[0]).values.reshape(-1, 1)
        log_test_data_set_ay = pd.read_csv('sencing_test_result/' + name_list[member_count] + '/log_' + log_num[log_count] + '.csv', usecols=[1]).values.reshape(-1, 1)
        log_test_data_set_az = pd.read_csv('sencing_test_result/' + name_list[member_count] + '/log_' + log_num[log_count] + '.csv', usecols=[2]).values.reshape(-1, 1)
        log_test_data_set_gx = pd.read_csv('sencing_test_result/' + name_list[member_count] + '/log_' + log_num[log_count] + '.csv', usecols=[3]).values.reshape(-1, 1)
        log_test_data_set_gy = pd.read_csv('sencing_test_result/' + name_list[member_count] + '/log_' + log_num[log_count] + '.csv', usecols=[4]).values.reshape(-1, 1)
        log_test_data_set_gz = pd.read_csv('sencing_test_result/' + name_list[member_count] + '/log_' + log_num[log_count] + '.csv', usecols=[5]).values.reshape(-1, 1)
        hash = 0
        while len(log_test_data_set_ax) > count:
            sec = time.time()
            
            # 枠内にデータを作成する
            test_data_set_ax = remake_test_data_set(test_data_set_ax, log_test_data_set_ax[count][0])
            test_data_set_ay = remake_test_data_set(test_data_set_ay, log_test_data_set_ay[count][0])
            test_data_set_az = remake_test_data_set(test_data_set_az, log_test_data_set_az[count][0])
            test_data_set_gx = remake_test_data_set(test_data_set_gx, log_test_data_set_gx[count][0])
            test_data_set_gy = remake_test_data_set(test_data_set_gy, log_test_data_set_gy[count][0])
            test_data_set_gz = remake_test_data_set(test_data_set_gz, log_test_data_set_gz[count][0])
        
            pick_dtw_ax_result = dtw.getDTW(train_data_set_ax, test_data_set_ax)
            pick_dtw_ay_result = dtw.getDTW(train_data_set_ay, test_data_set_ay)
            pick_dtw_gz_result = dtw.getDTW(train_data_set_gz, test_data_set_gz)

            drop_dtw_ax_result = dtw.getDTW(drop_train_data_set_ax, test_data_set_ax)
            drop_dtw_ay_result = dtw.getDTW(drop_train_data_set_ay, test_data_set_ay)
            drop_dtw_gz_result = dtw.getDTW(drop_train_data_set_gz, test_data_set_gz)

            hand_down_dtw_az_result = dtw.getDTW(hand_down_data_set_az, test_data_set_az)

            hand_up_dtw_az_result = dtw.getDTW(hand_up_data_set_az, test_data_set_az)

            waiper_left_ax_result = dtw.getDTW(waiper_left_data_set_ax, test_data_set_ax)
            waiper_left_ay_result = dtw.getDTW(waiper_left_data_set_ay, test_data_set_ay)
            waiper_left_gz_result = dtw.getDTW(waiper_left_data_set_gz, test_data_set_gz)

            waiper_right_ax_result = dtw.getDTW(waiper_right_data_set_ax, test_data_set_ax)
            waiper_right_ay_result = dtw.getDTW(waiper_right_data_set_ay, test_data_set_ay)
            waiper_right_gz_result = dtw.getDTW(waiper_right_data_set_gz, test_data_set_gz)
            flag = "test"
           
            
            if operation_identification(pick_dtw_gz_result - drop_dtw_gz_result) == "pick" and pick_dtw_ax_result < 17:
                flag = "pick"
                pick_count += 1
                insert_log_data(name_list[member_count], log_num[log_count], log_test_data_set_ax[count][0], log_test_data_set_ay[count][0], log_test_data_set_az[count][0], log_test_data_set_gx[count][0], log_test_data_set_gy[count][0], log_test_data_set_gz[count][0], 0, 0, 0, 0, 0, pick_dtw_gz_result, pick_dtw_gz_result - drop_dtw_gz_result, flag)
                test_data_set_ax = np.zeros_like(test_data_set_ax)
                test_data_set_ay = np.zeros_like(test_data_set_ay)
                test_data_set_az = np.zeros_like(test_data_set_az)
                test_data_set_gx = np.zeros_like(test_data_set_gx)
                test_data_set_gy = np.zeros_like(test_data_set_gy)
                test_data_set_gz = np.zeros_like(test_data_set_gz)

                
            elif operation_identification(pick_dtw_gz_result - drop_dtw_gz_result) == "drop" and drop_dtw_ax_result < 7:
                flag = "drop"
                drop_count += 1
                insert_log_data(name_list[member_count], log_num[log_count], log_test_data_set_ax[count][0], log_test_data_set_ay[count][0], log_test_data_set_az[count][0], log_test_data_set_gx[count][0], log_test_data_set_gy[count][0], log_test_data_set_gz[count][0], 0, 0, 0, 0, 0, drop_dtw_gz_result, pick_dtw_gz_result - drop_dtw_gz_result, flag)
                test_data_set_ax = np.zeros_like(test_data_set_ax)
                test_data_set_ay = np.zeros_like(test_data_set_ay)
                test_data_set_az = np.zeros_like(test_data_set_az)
                test_data_set_gx = np.zeros_like(test_data_set_gx)
                test_data_set_gy = np.zeros_like(test_data_set_gy)
                test_data_set_gz = np.zeros_like(test_data_set_gz)

            elif waiper_operation_identification(waiper_left_gz_result - waiper_right_gz_result, log_test_data_set_ax[count][0], test_data_set_ax[0][0]) == "waiper left" and waiper_left_ax_result < 12:
                flag = "waiper left"
                waiper_left_count += 1
                insert_log_data(name_list[member_count], log_num[log_count], log_test_data_set_ax[count][0], log_test_data_set_ay[count][0], log_test_data_set_az[count][0], log_test_data_set_gx[count][0], log_test_data_set_gy[count][0], log_test_data_set_gz[count][0], 0, 0, 0, 0, 0, waiper_left_gz_result, waiper_left_gz_result - waiper_right_gz_result, flag)
                test_data_set_ax = np.zeros_like(test_data_set_ax)
                test_data_set_ay = np.zeros_like(test_data_set_ay)
                test_data_set_az = np.zeros_like(test_data_set_az)
                test_data_set_gx = np.zeros_like(test_data_set_gx)
                test_data_set_gy = np.zeros_like(test_data_set_gy)
                test_data_set_gz = np.zeros_like(test_data_set_gz)
            elif waiper_operation_identification(waiper_left_gz_result - waiper_right_gz_result, log_test_data_set_ax[count][0], test_data_set_ax[0][0]) == "waiper right" and waiper_right_ax_result < 13:
                if waiper_right_gz_result < 3600:
                    flag = "waiper right"
                    waiper_right_count += 1
                    insert_log_data(name_list[member_count], log_num[log_count], log_test_data_set_ax[count][0], log_test_data_set_ay[count][0], log_test_data_set_az[count][0], log_test_data_set_gx[count][0], log_test_data_set_gy[count][0], log_test_data_set_gz[count][0], 0, 0, 0, 0, 0, waiper_right_gz_result, waiper_left_gz_result - waiper_right_gz_result, flag)
                    test_data_set_ax = np.zeros_like(test_data_set_ax)
                    test_data_set_ay = np.zeros_like(test_data_set_ay)
                    test_data_set_az = np.zeros_like(test_data_set_az)
                    test_data_set_gx = np.zeros_like(test_data_set_gx)
                    test_data_set_gy = np.zeros_like(test_data_set_gy)
                    test_data_set_gz = np.zeros_like(test_data_set_gz)

            elif hand_down_dtw_az_result < 8:
                print("hand down")
                test_data_set_ax = np.zeros_like(test_data_set_ax)
                test_data_set_ay = np.zeros_like(test_data_set_ay)
                test_data_set_az = np.zeros_like(test_data_set_az)
                test_data_set_gx = np.zeros_like(test_data_set_gx)
                test_data_set_gy = np.zeros_like(test_data_set_gy)
                test_data_set_gz = np.zeros_like(test_data_set_gz)
                flag = "hand down"
                hand_down_count += 1
                insert_log_data(name_list[member_count], log_num[log_count], log_test_data_set_ax[count][0], log_test_data_set_ay[count][0], log_test_data_set_az[count][0], log_test_data_set_gx[count][0], log_test_data_set_gy[count][0], log_test_data_set_gz[count][0], 0, 0, hand_down_dtw_az_result, 0, 0, 0, 0, flag)
                    
            elif hand_up_dtw_az_result < 9:
                print("hand up")
                hand_up_count += 1
                test_data_set_ax = np.zeros_like(test_data_set_ax)
                test_data_set_ay = np.zeros_like(test_data_set_ay)
                test_data_set_az = np.zeros_like(test_data_set_az)
                test_data_set_gx = np.zeros_like(test_data_set_gx)
                test_data_set_gy = np.zeros_like(test_data_set_gy)
                test_data_set_gz = np.zeros_like(test_data_set_gz)
                flag = "hand up"
                insert_log_data(name_list[member_count], log_num[log_count], log_test_data_set_ax[count][0], log_test_data_set_ay[count][0], log_test_data_set_az[count][0], log_test_data_set_gx[count][0], log_test_data_set_gy[count][0], log_test_data_set_gz[count][0], 0, 0, hand_up_dtw_az_result, 0, 0, 0, 0, flag)            
                time.sleep(1)
            
            
            else:
                flag = "not jestur"
                insert_log_data(name_list[member_count], log_num[log_count], log_test_data_set_ax[count][0], log_test_data_set_ay[count][0], log_test_data_set_az[count][0], log_test_data_set_gx[count][0], log_test_data_set_gy[count][0], log_test_data_set_gz[count][0], 0, 0, 0, 0, 0, 0, 0, flag)

            print("動作なし")
            count += 1
            pick_dtw_gx_list = []
            pick_dtw_gy_list = []
            drop_dtw_gx_list = []
            drop_dtw_gy_list = []
            tt += 1
            elapsed_time = time.time()
            print("time")
            print(elapsed_time - sec)
            print("count")
            print(count)

        with open('sencing_test_result/' + name_list[member_count] + '/comparative_log_num_1.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerow(['pick count=', pick_count, 'drop count=', drop_count, 'waiper_left_count=', waiper_left_count, 'waiper_right_count=', waiper_right_count, 'hand down count=', hand_down_count, 'hand up count = ', hand_up_count, '最終データの集計結果です', log_count])

        count = 0
        log_count += 1
          
        print("pick")
        print(pick_count)
        print("drop")
        print(drop_count)
        print("waiper left")
        print(waiper_left_count)
        print("waiper right")
        print(waiper_right_count)
        print("hand down")
        print(hand_down_count)
        print("hand up")
        print(hand_up_count)
        pick_count = 0
        drop_count = 0
        waiper_left_count = 0
        waiper_right_count = 0
        hand_down_count = 0
        hand_up_count = 0

        print("====================================================================================")
        print("====================================================================================")
        print("次のログファイルで再実験を開始します.")
        print("====================================================================================")
        print("====================================================================================")
        time.sleep(1)
        
    log_count = 0
    member_count += 1
    print("====================================================================================")
    print("====================================================================================")
    print("次のメンバーログファイルで再実験を開始します.")
    print("====================================================================================")
    print("====================================================================================")
    time.sleep(1)

