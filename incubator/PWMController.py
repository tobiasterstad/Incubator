__author__ = 'tobias'

import threading
import logging
from Queue import Queue

try:
    from servopi.ABE_ServoPi import PWM
    from smbus import SMBus
except ImportError:
    print("Failed to init PWMCOntroller. ")
    debug = True
    from devmocks import GPIO, SMBus, PWM


class PWMController(threading.Thread):

    def __init__(self, q):
        self.pwm = PWM(SMBus(1), 0x60)
        self.pwm.set_pwm_freq(50)
        self.pwm.output_enable()
        self.q = q

        threading.Thread.__init__(self)
        self.running = False

    def run(self):
        logging.info("Starting PWM Controller")
        self.running = True

        while self.running:
            try:
                a = self.q.get(True, 5)

                logging.debug("Received: "+a)
                if a is None:
                    self.running = False

                if a == "exit":
                    self.running = False

                split = a.split(":")
                adr = split[0]
                value = split[1]

                self.pwm.set_pwm(int(adr), 0, int(value))

            except:
                None

        logging.info("Stopped PWM Controller")

    def stop(self):
        self.running = False