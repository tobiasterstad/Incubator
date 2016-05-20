__author__ = 'tobias'
# coding=UTF-8

from datetime import *
import time

class State:
    def __init__(self):
        self.temp1 = 20
        self.temp2 = 20
        self.humidity = 20
        self.pid = 0
        self.day = 1
        self.ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        self.humidity_level = 0

    def update_ts(self):
        self.ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def set_temp1(self, temp1):
        self.temp1 = temp1

    def set_temp2(self, temp2):
        self.temp2 = temp2

    def set_humidity(self, humidity):
        self.humidity = humidity

    def get_temp1(self):
        return self.temp1

    def get_temp2(self):
        return self.temp2

    def get_humidity(self):
        return self.humidity

    def set_pid(self, pid):
        self.pid = pid

    def get_pid(self):
        return self.pid

    def get_ts(self):
        return self.ts

    def set_day(self, day):
        self.day = day

    def get_day(self):
        return self.day

    def set_humidity_level(self, humidity_level):
        self.humidity_level = humidity_level

    def get_humidity_level(self):
        return self.humidity_level