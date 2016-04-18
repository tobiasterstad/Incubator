__author__ = 'tobias'


from servopi.ABE_ServoPi import PWM
import smbus
import threading
import time
import logging


class PWMController(threading.Thread):

    def __init__(self, q):
        self.pwm = PWM(smbus.SMBus(1), 0x60)
        self.pwm.set_pwm_freq(50)
        self.pwm.output_enable()
        self.q = q

        threading.Thread.__init__(self)
        self.running = False

    def run(self):
        logging.info("Starting PWM Controller")
        self.running = True

        while self.running:
            a = self.q.get(True)

            logging.debug("Received: "+a)
            if a is None:
                self.running = False

            if a == "exit":
                self.running = False

            split = a.split(":")
            adr = split[0]
            value = split[1]

            self.pwm.set_pwm(int(adr), 0, int(value))

            time.sleep(0.1)

        logging.info("Stopping PWM Controller")

    def stop(self):
        self.running = False