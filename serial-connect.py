import serial

dev = "/dev/rfcomm0"
rate = 9600
ser = serial.Serial(dev, rate, timeout=10)
def serial_send():
    data = "hello"
    data += "\r\n"
    ser.write(data)
    print "============================"

def serial_read():
    res = ser.readline(10000)
    res = res.encode()
    print "------------------"
    print res

beContinue = True

beSend = True
 
serial_send()

