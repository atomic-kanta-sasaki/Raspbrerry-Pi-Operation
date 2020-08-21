# -*- coding: utf-8 -*-

from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

def getDTW(train_data_set, test_data_set):
    distance, path = fastdtw(train_data_set, test_data_set)
#    print (distance)
    return distance

def main():
    getDTW(train_data_set, test_data_set)

if __name__ == '__main__':
    main()
