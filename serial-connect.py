# coding: UTF-8

import serial
import csv
import pandas as pd

dev = "/dev/rfcomm0"
rate = 9600
ser = serial.Serial(dev, rate, timeout=10)
def serial_send():
    data = "hello"
    # data = "https://www.google.com"
    data += "\r\n"

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

# def updataCsv():


beContinue = True

beSend = True
 
serial_send()

read_text = serial_read()
read_text = sentenceShaping(read_text)
print "取得したデータを書き込みます"
# writeCsv(read_text)

print "CSVファイルを読み込みます"
readCsv()
