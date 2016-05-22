__author__ = 'tobias'

import random

class GPIO:

    OUT = 1
    BOARD = None
    HIGH = None
    LOW = None

    def __init__(self):
        None

    @staticmethod
    def setmode(param):
        None

    @staticmethod
    def setup(pin, OUT):
        None

    @staticmethod
    def output(p1, p2):
        None


class SMBus:

    def __init__(self, param):
        None

    def write_byte_data(self, p1, p2, p3):
        None

    def write_byte(self, p1, p2):
        None


class PWM:
    def __init__(self, p1, p2):
        None

    def set_pwm_freq(self, p1):
        None

    def output_enable(self):
        None

    def set_pwm(self, p1, p2, p3):
        None


class HTU21D:
    def __init__(self):
        None

    def read_temperature(self):
        return 37.3

    def read_humidity(self):
        return 53


class TempSensor:
    debug_temp = 37.5

    def __init__(self):
        None

    def read_temp(self):

        if self.debug_temp < 37:
            rand = random.randint(-1, 10) * 0.1
        else:
            rand = random.randint(-1, 1) * 0.1

        self.debug_temp += rand
        return self.debug_temp