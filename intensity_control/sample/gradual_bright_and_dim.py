# DOWNLOAD GPIO MODULE HERE: https://pypi.python.org/pypi/RPi.GPIO
# EXTRACT, AND TYPE THE FOLLOWING COMMAND IN THE DIRECTORY
# sudo python3 setup.py install

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(21, GPIO.OUT) # SET OUTPUT TO PIN 21

pwm = GPIO.PWM(21, 50)
pwm.start(0)

try:
    while True:
        #BRIGHT
        for i in range(100):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.02)
        #DIM
        for i in range(100):
            pwm.ChangeDutyCycle(100 - i)
            time.sleep(0.02)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
pwm.stop()
GPIO.cleanup()