# coding: UTF-8

import serial
import csv
import pandas as pd

dev = "/dev/rfcomm0"
rate = 9600
ser = serial.Serial(dev, rate, timeout=10)
new_url_list = []

def serial_send(flag):
    ser.write(data)
    print "============================"

def serial_read():
    res = ser.readline(10000)
    print "---------------------------"
    print res
    return res

def sentenceShaping(text):
    shaping_text = text.strip().decode('utf-8')
    return shaping_text

def writeCsv(url):
    with open('url.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow([url])

def readCsv():
    with open("url.csv") as f:
        for row in csv.reader(f):
            print row

def updataCsv(new_url_list):
   with open("url.csv", 'w') as f:
       writer = csv.writer(f)
       writer.writerow()

def getValidUrlIndex():
    with open("url.csv") as f:
        for index, row in enumerate(csv.reader(f)):
            if row == "end":
                return index

def createNewUrlList():
    with open("url.csv") as f:
        for row in csv.reader(f):
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

    print "CSVファイルを読み込みます"
    readCsv()
