__author__ = 'tobias'
# coding=UTF-8

from ABElectronics_ServoPi import PWM
from datetime import datetime
import time


servoMin = 170  # Min pulse length out of 4096
servoMax = 450  # Max pulse length out of 4096


class Roller:

    def __init__(self):
        self.pwm = PWM(0x40)
        self.pwm.setPWMFreq(50)
        self.pwm.outputEnable()
        self.direction = 0
        self.roll_time = datetime.today()

    def roll(self):
        print "Roll eggs"
        self.roll_time = datetime.today()

        if self.direction == 0:
            self.roll_left()
            self.direction = 1
        else:
            self.roll_right()
            self.direction = 0

    def roll_left(self):
        for i in range(servoMin, servoMax, 1):
            self.pwm.setPWM(0, 0, i)
            time.sleep(0.05)

    def roll_right(self):
        for i in range(servoMax, servoMin, -1):
            self.pwm.setPWM(0, 0, i)
            time.sleep(0.05)

    # Get the number of hours since last flip
    def get_minutes_from_last_roll(self):
        diff2 = datetime.today()-self.roll_time
        return int(diff2.total_seconds()/60)

    def is_time_to_role(self, day, config):
        last_roll = self.get_minutes_from_last_roll()

        if 1 <= day <= 18 and last_roll >= config.get_roll_intervall():
            return True

        return False
