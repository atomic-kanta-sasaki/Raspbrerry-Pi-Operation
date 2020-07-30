# coding: utf-8
import subprocess as spc

# MACアドレスをリストに追加
MAC_Address_List = ["D0:57:7B:20:46:ED", "00:28:F8:AA:6B:3E"]

# MACアドレスをKeyとする辞書を作成
mydict = {"D0:57:7B:20:46:ED": "", "00:28:F8:AA:6B:3E": ""}

# RSSIを取得するShellをたたく場所を作成
res=spc.check_output("getsi")

# 以下取得したデータを整形する
res = res.split("\n")

dict1_rssi = [row for row in res if 'D0:57:7B:20:46:ED' in row]

dict2_rssi = [row for row in res if '00:28:F8:AA:6B:3E' in row]

dict1_rssi = dict1_rssi[0].split(" ")
dict2_rssi = dict2_rssi[0].split(" ")

rssi_1 = dict1_rssi[6]
rssi_2 = dict2_rssi[6]

mydict["D0:57:7B:20:46:ED"] = rssi_1
mydict["00:28:F8:AA:6B:3E"] = rssi_2

print mydict

