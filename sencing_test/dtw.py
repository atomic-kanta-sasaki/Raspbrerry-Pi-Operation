# -*- coding: utf-8 -*-

from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from matplotlib import pyplot as plt
import numpy as np

def getDTW(train_data_set, test_data_set):
    distance, path = fastdtw(train_data_set, test_data_set)
#    print (distance)
    return distance

def getDTWPath(x, y):
    distance, path = fastdtw(x, y, dist=euclidean)
    plt.plot(x, label='x')
    plt.plot(y, label='y')
    for x_, y_ in path:
        plt.plot([x_, y_], [x[x_], y[y_]], color='gray', linestyle='dotted', linewidth=1)
    plt.legend()
    plt.title('Our two temporal sequences')
    plt.show()
    return path

def main():
    getDTW(train_data_set, test_data_set)

if __name__ == '__main__':
    main()
