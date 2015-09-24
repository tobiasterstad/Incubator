__author__ = 'tobias'

import RPi.GPIO as GPIO
import threading
import time


class SSRRegulator(threading.Thread):

    def __init__(self):

        # Pin 11 or 7
        self.pin = 11

        # use P1 header pin numbering convention
        GPIO.setmode(GPIO.BOARD)

        # Set up the GPIO channels - one input and one output
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)

        threading.Thread.__init__(self)
        self.value = 125.0

        # 20 Sek cycle
        self.cycle = 20.0

        # 400 steps
        self.steps = 400.0

        self._running = True

    def run(self):
        print "Starting SSRRegulator"
        while self._running:
            step = self.cycle/self.steps
            on = self.value * step
            off = self.cycle - on

            # print "ON: Value: ", self.value, ", ON: ", on, ", OFF: ", off
            GPIO.output(self.pin, GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
            time.sleep(on)
            GPIO.output(self.pin, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            # print "OFF"
            time.sleep(off)

        print "Stopping SSRRegulator"

    def stop(self):
        self._running = False
        print("stopping..")

    def set_value(self, value):
        if value > self.steps:
            raise ValueError('Value too high: '+str(value)+'. Expected 0 - '+str(self.steps))
        if value < 0:
            raise ValueError('Value too low.Expected 0 - '+str(self.steps))

        self.value = value

    def get_value(self):
        return self.value