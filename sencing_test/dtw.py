# -*- coding: utf-8 -*-

import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from matplotlib import pyplot as plt
import pandas as pd

# def data_frame(data):
#     for 

# 異なる2種類のデータを定義
x = pd.read_csv('sample.csv', usecols=[0]).values.reshape(-1, 1)
y_init = pd.read_csv('experimental_data.csv', usecols=[0]).values.reshape(-1, 1)
y = y_init[0:128]
#print(len(y))
#index = 1
# for item in range(129, len(y_init)):
#     # DTWを計算
#     distance, path = fastdtw(x, y, dist=euclidean)
#     print ('===================')
#     print (distance)
#     print('===================')
#     y = y_init[index : item]
#     index += 1

#distance, path = fastdtw(x, y, dist=euclidean)
#print ('===================')
#print (distance)
#print(path)
#print('===================')
# y = y_init[index : item]



#plt.plot(x, label='x')
#plt.plot(y, label='y')

#df_1 = pd.read_csv('sample.csv', usecols=[0])

# 各点がどのように対応しているかを図示する
#for x_, y_ in path:
#   plt.plot([x_, y_], [x[x_], y[y_]], color='gray', linestyle='dotted', linewidth=1)
#   plt.legend()
#   plt.title('Our two temporal sequences')
#   plt.show()

def getDTW(train_data_set, test_data_set):
    distance, path = fastdtw(train_data_set, test_data_set)
#    print (distance)
    return distance

def main():
    getDTW(train_data_set, test_data_set)

if __name__ == '__main__':
    main()
