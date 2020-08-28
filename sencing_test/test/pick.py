# coding: UTF-8

import serial
import csv
import pandas as pd
#import scan
import sencing

# MAC_Address_1に接続するためのシリアル
 # MAC_Address_1に接続するためのシリアル
dev = "/dev/rfcomm0"
rate = 9600
ser_1 = serial.Serial(dev, rate, timeout=10)

# MAC_Address_2に接続するためのシリアル
#dev = "/dev/rfcomm1"
#rate = 9600
#ser_2 = serial.Serial(dev, rate, timeout=10)

new_url_list = []
# 使用するMACアドレスを変数化
MAC_Address_1 = "1C:BF:C0:2B:52:D2"
MAC_Address_2 = "00:28:F8:AA:6B:3E" 

"""
シリアル通信でURLORフラグを送信する

@param flag or url
"""
def serial_send(ser, data):
    ser.write(data)
    print "============================"

"""
シリアル通信でデータを読み込む

@return 受信データ

"""
def serial_read(ser):
    res = ser.readline(10000)
    print "---------------------------"
    print res
    return res

"""
シリアル通信で送られてきたデータを使用できる形に整形する

@param シリアルデータ
@return 整形後データ
"""
def sentenceShaping(text):
    shaping_text = text.strip().decode('utf-8')
    return shaping_text

"""
csvファイルにurlを書き込む

@param url
"""
def writeCsv(url):
    with open('url.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow([url])

"""
送信すべきデータをcsvファイルから取得する

@return  送信データ
"""
def readCsv():
    with open("url.csv") as f:
        for row in csv.reader(f):
            return row[0]
            break

"""
現在のCSVファイルをコンソールに表示する
"""
def printCsvContents():
    with open("url.csv") as f:
        for row in csv.reader(f):
            print row

"""
csvファイルを更新する

@param new_url_list
"""
def updataCsv(new_url_list):
    with open("url.csv", 'w') as f:
        writer = csv.writer(f)
        for row in new_url_list:
            writer.writerow(row)
"""
有効なURLが入っているindex番号を返す

@return index
"""
def getValidUrlIndex():
    with open("url.csv") as f:
        for index, row in enumerate(csv.reader(f)):
            if row == "end":
                return index

"""
Drop後新しい更新用のURLリストを作成する

@return new_url_list
"""
def createNewUrlList():
    with open("url.csv") as f:
        for row in csv.reader(f):
            print "row"
            print row
            print row[0]
            new_url_list.append(row)
        
        del new_url_list[0]
        return new_url_list

def main():
    print('sdlkjfla;jsd;l')
    data = str('1')
    data += "\r\n"
    #rssi_dict = scan.RSSI_Scan(MAC_Address_1, MAC_Address_2)
    # MACアドレスの２が大きいとき
    serial_send(ser_1, data)
    read_text = serial_read(ser_1)
    # 受信時にいろいろいらないものがくっついてくるため整形する
    read_text = sentenceShaping(read_text)

    print "取得したデータを書き込みます"
    writeCsv(read_text)

    print "現在のCSvファイルの情報"
    printCsvContents()
    sencing

if __name__ == '__main__':
    main()
