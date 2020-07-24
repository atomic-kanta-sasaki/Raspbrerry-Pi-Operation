# coding: UTF-8

import serial
import csv
import pandas as pd

dev = "/dev/rfcomm0"
rate = 9600
ser = serial.Serial(dev, rate, timeout=10)
new_url_list = []

"""
シリアル通信でURLORフラグを送信する

@param flag or url
"""
def serial_send(flag):
    ser.write(data)
    print "============================"

"""
シリアル通信でデータを読み込む

@return 受信データ

"""
def serial_read():
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

beContinue = True

beSend = True

print "select 1 or 2 :1 is pick 2is drop "
select = int(raw_input())
if select == 1:
    data = "hello"
    data += "\r\n"
    serial_send(data)

    read_text = serial_read()
    read_text = sentenceShaping(read_text)

    print "取得したデータを書き込みます"
    writeCsv(read_text)

    print "現在のCSvファイルの情報"
    printCsvContents()

elif select == 2:
    data = readCsv()
    print data
    data += "\r\n"
    serial_send(data)
    new_list = createNewUrlList()
    updataCsv(new_list)
    print "更新されたURLリスト"
    print new_list

    print "現在のCSVファイルの情報"
    printCsvContents()


