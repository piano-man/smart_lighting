import serial, time
arduino = serial.Serial('/dev/ttyACM0', 9600,timeout=2)
time.sleep(1) #give the connection a second to settle
#arduino.write("Hello from Python!")
while True:
	data = (str(arduino.readline()))
	print(data)
