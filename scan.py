# coding: utf-8
import subprocess as spc

MAC_Address_1 = "D0:57:7B:20:46:ED"
MAC_Address_2 = "00:28:F8:AA:6B:3E"

# MACアドレスをKeyとする辞書を作成
mydict = {MAC_Address_1: "", MAC_Address_2: ""}

# RSSIを取得するShellをたたく場所を作成
res=spc.check_output("getsi")

# 以下取得したデータを整形する
res = res.split("\n")

dict1_rssi = [row for row in res if MAC_Address_1 in row]

dict2_rssi = [row for row in res if MAC_Address_2 in row]

print dict1_rssi
print dict2_rssi

dict1_rssi = dict1_rssi[0].split(" ")
dict2_rssi = dict2_rssi[0].split(" ")

rssi_1 = dict1_rssi[6]
rssi_2 = dict2_rssi[6]

mydict[MAC_Address_1] = rssi_1
mydict[MAC_Address_2] = rssi_2

print mydict

