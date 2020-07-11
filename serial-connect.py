import serial

dev = "/dev/rfcomm0"
rate = 9600
ser = serial.Serial(dev, rate, timeout=10)
def serial_send():
    string = "hello world"
    string = string + "\r\n"
    ser.write(string)

def serial_read():
    res = ser.readline(10000)
    res = res.encode()
    print res

serial_read()
