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
    print "---------------------------"
    print res
    return res

def sentenceShaping(text):
    shaping_text = text.strip().decode('utf-8')
    return shaping_text

beContinue = True

beSend = True
 
serial_send()

read_text = serial_read()
read_text = sentenceShaping(read_text)
print read_text
