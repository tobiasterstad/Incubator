__author__ = 'tobias'

import glob
import random
import time
import os


class TempSensor:
    def __init__(self):

        self.debug = 0

        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')


        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def get_temp(self):
        pass

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        if self.debug == 1:
            global debug_temp

            if debug_temp < 37:
                rand = random.randint(-1, 10) * 0.1
            else:
                rand = random.randint(-1, 1) * 0.1

            debug_temp = debug_temp + rand
            return debug_temp

        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return round(temp_c, 1)
