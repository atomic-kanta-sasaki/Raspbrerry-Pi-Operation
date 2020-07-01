import serial

comport = serial.Serial('com8', baudrate=19200, parity=serial.PARITY_NONE)
recv_data = comport.read(12)
meas_data = float(recv_data.decode('utf-8').split('+')[1])
print(meas_data)
comport.close()
