import serial

dev = "/dev/rfcomm0"
rate = 9600
ser = serial.Serial(dev, rate, timeout=10)

string = "hello world"
string = string + "\r\n"

ser.write(string)
res = ser.readline(10000)
res = res.encode()
print res
