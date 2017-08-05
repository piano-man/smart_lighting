#!/usr/bin/python3
'''LIGHT INTENSITY MEASUREMENT USING GY30 (BH1750)'''

import time
import logging
import smbus

class GY30(object):
    '''IMPLEMENT GY30 LIGHT SENSOR LIBRARY'''

    # DEFINE CONSTANTS
    POWER_DOWN = 0x00   # No active state
    POWER_ON = 0x01     # Power on
    RESET = 0x07        # Reset data register value
    DEVICE = 0x23       # Default device I2C Address

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

    def __init__(self, bus, addr=DEVICE):
        '''CONSTRUCTOR'''
        self.bus = bus
        self.addr = addr
        self.power_down()
        self.set_sensitivity()

    def set_mode(self, mode):
        '''SETS THE BUS MODE'''
        self.mode = mode
        self.bus.write_byte(self.addr, self.mode)

    def power_down(self):
        '''POWER DOWN MODE'''
        self.set_mode(self.POWER_DOWN)

    def power_on(self):
        '''POWER ON MODE'''
        self.set_mode(self.POWER_ON)

    def reset(self):
        '''MODE RESET'''
        self.power_on() #It has to be powered on before resetting
        self.set_mode(self.RESET)

    def cont_low_res(self):
        '''CONTINUOUS LOW RESOLUTION MODE'''
        self.set_mode(self.CONTINUOUS_LOW_RES_MODE)

    def cont_high_res(self):
        '''CONTINUOUS HIGH RESOLUTION MODE'''
        self.set_mode(self.CONTINUOUS_HIGH_RES_MODE_1)

    def cont_high_res2(self):
        '''CONTINUOUS HIGH RESOLUTION MODE 2'''
        self.set_mode(self.CONTINUOUS_HIGH_RES_MODE_2)

    def oneshot_low_res(self):
        '''ONE TIME LOW RESOLUTION MODE'''
        self.set_mode(self.ONE_TIME_LOW_RES_MODE)

    def oneshot_high_res(self):
        '''ONE TIME HIGH RESOLUTION MODE'''
        self.set_mode(self.ONE_TIME_HIGH_RES_MODE_1)

    def oneshot_high_res2(self):
        '''ONE TIME HIGH RESOLUTION MODE 2'''
        self.set_mode(self.ONE_TIME_HIGH_RES_MODE_2)

    def set_sensitivity(self, sensitivity=69):
        '''
        SETS THE SENSOR SENSITIVITY
        VALID RANGE : 31 - 254
        DEFAULT     : 69
        '''
        if sensitivity < 31:
            self.mtreg = 31
        elif sensitivity > 254:
            self.mtreg = 254
        else:
            self.mtreg = sensitivity
        self.power_on()
        self.set_mode(0x40 | (self.mtreg >> 5))
        self.set_mode(0x60 | (self.mtreg & 0x1f))
        self.power_down()

    def get_result(self):
        '''
        RETURNS CURRENT MEASUREMENT RESULT (in lx)
        MODE COEFFICIENTS:
            1 : HIGH RESOLUTION MODE
            2 : HIGH RESOLUTION MODE 2
            3 : LOW RESOLUTION MODE
        '''
        data = self.bus.read_word_data(self.addr, self.mode)
        count = data >> 8 | (data & 0xff) << 8
        mode_coeff = 2 if (self.mode & 0x03) == 0x01 else 1
        ratio = 1 / (1.2 * (self.mtreg / 69.0) * mode_coeff)
        return ratio * count

    def wait_for_result(self, additional=0):
        '''GENERATES INTENSITY RESULT'''
        base_time = 0.018 if (self.mode & 0x03) == 0x03 else 0.128
        time.sleep(base_time * (self.mtreg / 69.0) + additional)

    def measure(self, mode, additional_delay=0):
        '''
        PERFORMS COMPLETE MEASUREMENT
        PARAMETERS USED : MODE, ADDITIONAL DELAY TIME
        OUTPUT          : INTENSITY (in lx)
        '''
        self.reset()
        self.set_mode(mode)
        self.wait_for_result(additional=additional_delay)
        return self.get_result()

    def measure_low_res(self, additional_delay=0):
        '''MEASURES INTENSITY IN ONE TIME LOW RESOLUTION MODE'''
        return self.measure(self.ONE_TIME_LOW_RES_MODE, additional_delay)

    def measure_high_res(self, additional_delay=0):
        '''MEASURES INTENSITY IN ONE TIME HIGH RESOLUTION MODE'''
        return self.measure(self.ONE_TIME_HIGH_RES_MODE_1, additional_delay)

    def measure_high_res2(self, additional_delay=0):
        '''MEASURES INTENSITY IN ONE TIME HIGH RESOLUTION MODE 2'''
        return self.measure(self.ONE_TIME_HIGH_RES_MODE_2, additional_delay)

def main():
    '''MAIN'''
    # UNCOMMENT FOR APPROPRIATE SMBUS
    # bus = smbus.SMBus(0) # Rev 1 Pi uses 0
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
    sensor = GY30(bus)

    while True:
        print('Sensitivity: {:d}'.format(sensor.mtreg))
        for measurefunc, name in [(sensor.measure_low_res, 'Low Res '),
                                  (sensor.measure_high_res, 'High Res '),
                                  (sensor.measure_high_res2, 'High Res 2')]:
            print('{} Light Level : {:3.2f} lx'.format(name, measurefunc()))
        print('--------')
        sensor.set_sensitivity((sensor.mtreg + 10) % 255)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
