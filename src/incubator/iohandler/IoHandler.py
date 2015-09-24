__author__ = 'tobias'

import threading
import time
import RPi.GPIO as GPIO


class IoHandler(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._running = False
        self.button1 = False
        self.button2 = False

        # TODO Change pins
        self.button1_pin = 17
        self.button2_pin = 18
        self.relay1_pin = 19
        self.relay2_pin = 20

        # Init GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button1_pin, GPIO.IN)
        GPIO.setup(self.button2_pin, GPIO.IN)
        GPIO.setup(self.relay1_pin, GPIO.OUT)
        GPIO.setup(self.relay2_pin, GPIO.OUT)

    @staticmethod
    def set_relay(value, pin):
        if value:
            GPIO.output(pin, 1)
        else:
            GPIO.output(pin, 0)

    def run(self):
        self._running = True
        while self._running:

            button1 = GPIO.input(self.button1_pin)
            if button1 != self.button1:
                self.button1 = button1
                self.set_relay(button1, self.relay1_pin)
                print("Button 1 Pressed")

            button2 = GPIO.input(self.button2_pin)
            if button2 != self.button2:
                self.button2 = button2
                self.set_relay(button2, self.relay2_pin)
                print("Button 2 Pressed")

            time.sleep(0.05)

    def stop(self):
        self._running = False