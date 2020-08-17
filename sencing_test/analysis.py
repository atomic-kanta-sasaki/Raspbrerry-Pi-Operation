#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_1 = pd.read_csv('sample.csv', usecols=[0])

df = pd.DataFrame(df_1)

df_2 = pd.read_csv('sample.csv',  usecols=[1])
df_3 = pd.read_csv('sample.csv',  usecols=[2])
df_4 = pd.read_csv('sample.csv',  usecols=[3])
df_5 = pd.read_csv('sample.csv',  usecols=[4])
df_6 = pd.read_csv('sample.csv', usecols=[5])

df.plot()


