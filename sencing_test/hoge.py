import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from matplotlib import pyplot as plt
# 異なる2種類のデータを定義
x = np.array([2, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
y = np.array([1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
# DTWを計算
distance, path = fastdtw(x, y, dist=euclidean)
print("DTW距離:", distance)
plt.plot(x, label='x')
plt.plot(y, label='y')
# 各点がどのように対応しているかを図示する
for x_, y_ in path:
  plt.plot([x_, y_], [x[x_], y[y_]], color='gray', linestyle='dotted', linewidth=1)
plt.legend()
plt.title('Our two temporal sequences')
plt.show()