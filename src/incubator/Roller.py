__author__ = 'tobias'
# coding=UTF-8


from datetime import datetime
import time
import threading

servoMin = 170  # Min pulse length out of 4096
servoMax = 450  # Max pulse length out of 4096


class Roller(threading.Thread):

    def __init__(self, q, roll_interval=60):

        self.q = q

        self.direction = 0
        self.roll_time = datetime.today()

        self.day = 1
        self.roll_interval = roll_interval

        threading.Thread.__init__(self)
        self.running = False

    def run(self):
        self.running = True
        i = 0
        while self.running:
            if 1 <= self.day <= 18 and i >= 600:
                self.roll()
                i = 0

            # Sleep 1 minute
            time.sleep(6)
            i += 1
        print "Stopping Roller"

    def stop(self):
        self.running = False

    def set_day(self, day):
        self.day = day

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
            # self.pwm.set_pwm(0, 0, i)
            self.q.put("0:"+i)
            time.sleep(0.05)

    def roll_right(self):
        for i in range(servoMax, servoMin, -1):
            # self.pwm.set_pwm(0, 0, i)
            self.q.put("0:"+i)
            time.sleep(0.05)

    # Get the number of hours since last flip
    def get_minutes_from_last_roll(self):
        diff2 = datetime.today()-self.roll_time
        return int(diff2.total_seconds()/60)
