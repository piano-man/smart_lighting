from urllib.parse import urlencode
from urllib.request import Request, urlopen
import smbus
import time
import subprocess
import requests
 
# Define some constants from the datasheet
 
DEVICE     = 0x23 # Default device I2C address
 
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
 
# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23
 
#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
 
def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number
  return ((data[1] + (256 * data[0])) / 1.2)
 
def readLight(addr=DEVICE):
  try:	
   data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
   return convertToNumber(data)
  except IOError:
    subprocess.call(['i2cdetect', '-y', '1'])
    flag = 1
 
def main():
 
  while True:
    print( "Light Level : " + str(readLight()) + " lx")
    print("done")
    url = 'http://172.20.18.16:5000/intensity'
    post_fields = {'intensity': str(readLight()),\
		'module_no': "23",\
		'pi_token':"test12345"}
    #request = Request(url, urlencode(post_fields).encode())
    r= requests.post(url,json=post_fields)
    print(r)
    
   
if __name__=="__main__":
   main()
