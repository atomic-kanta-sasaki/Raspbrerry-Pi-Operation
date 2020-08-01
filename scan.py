# coding: utf-8
import subprocess as spc
import serial

MAC_Address_1 = "1C:BF:C0:2B:52:D2"
MAC_Address_2 = "00:28:F8:AA:6B:3E"
dev = "/dev/rfcomm0"
rate = 9600
ser_1 = serial.Serial(dev, rate, timeout=10)

dev = "/dev/rfcomm1"
rate = 9600
ser_2 = serial.Serial(dev, rate, timeout=10)

"""
特定のMACアドレスのRSSIを取得し辞書型で返す

@param MAC_Address_1
@param MAC_Address_2

@return RSSI_dict
"""
def RSSI_Scan(MAC_Address_1, MAC_Address_2):

    # MACアドレスをKeyとする辞書を作成
    RSSI_dict = {MAC_Address_1: "", MAC_Address_2: ""}

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

    RSSI_dict[MAC_Address_1] = rssi_1
    RSSI_dict[MAC_Address_2] = rssi_2

    print RSSI_dict
    return RSSI_dict

"""
キャリブレーションの際に必要なRSSI値の差を返却する

@param RSSI_1
@param RSSI_2

@return difference
"""
def Calibration(RSSI_1, RSSI_2):
    difference = RSSI_1 - RSSI_2
    
    return difference

def serial_send(ser):
    data = "hello"
    data += "\r\n"
    ser.write(data)
    print "============================"

rssi_dict = RSSI_Scan(MAC_Address_1, MAC_Address_2)

if rssi_dict[MAC_Address_1] < rssi_dict[MAC_Address_2]:
    serial_send(ser_1)
else:
    serial_send(ser_2)

def main():
    RSSI_Scan(MAC_Address_1, MAC_Address_2)


if __name__ == '__main__':
    main()
