__author__ = 'tobias'
# coding=UTF-8

from PID import *
from Roller import *
from TempSensor import TempSensor
from Dimmer import Dimmer

import time
import sys
import datetime

debug = 0
debug_temp = 20.1


def init():
    print "Init hatcher"


# Get the number of days since start
def get_days_from_start():
    d = datetime.datetime.fromtimestamp(start_time)
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).day - d.day + 1


# Get the number of hours since last flip
def get_minutes_from_last_roll():
    diff = time.time() - roll_time
    minutes_from_roll = int(diff / 60.0)
    #print "hours from roll " + str(minutes_from_roll)
    return minutes_from_roll




start_time = time.time()
roll_time = time.time()
print "Äggmaskinen startar " + datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
init()

p = PID(5.0, 0.5, 1.0)
p.setPoint(37.5)

roller = Roller()
tempSensor = TempSensor()
dimmer = Dimmer(debug)

while True:
    day = get_days_from_start()
    last_roll = get_minutes_from_last_roll()

    if 1 <= day <= 18 and last_roll > 120:
        print "Vända ägg"
        roll_time = time.time()
        roller.roll()

    temp = tempSensor.read_temp()
    pid = p.update(temp)
    dimmer.dim(pid)

    print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ", " + str(temp) + ", " + str(pid) + ", " + str(day) + ", " + last_roll)
    sys.stdout.flush()
    time.sleep(15)