__author__ = 'tobias'

import RPi.GPIO as GPIO
import threading
import time
import logging


class SSRRegulator(threading.Thread):

    def __init__(self):

        self.kp = 100.0
        self.ki = 1.0

        self.integral = 0
        self.expected_value = 0.0

        self.pid_max = 400
        self.pid_min = 0
        self.f1 = open('/var/www/pid.php', 'w+')

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
        self.cycle = 5.0

        # 400 steps
        self.steps = 400.0

        self._running = True

    def run(self):
        logging.info("Starting SSRRegulator")
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

        logging.info("Stopping SSRRegulator")

    def stop(self):
        self._running = False

    def set_value(self, value):
        if value > self.steps:
            raise ValueError('Value too high: '+str(value)+'. Expected 0 - '+str(self.steps))
        if value < 0:
            raise ValueError('Value too low.Expected 0 - '+str(self.steps))

        self.value = value

    def get_value(self):
        return self.value

    def set_point(self, value=1.0):
        self.expected_value = value

    def set_k(self, k):
        self.kp = k

    def set_i(self, i):
        self.ki = i

    def within_min_max(self, output):
        if output > self.pid_max:
            output = self.pid_max
        if output < self.pid_min:
            output = self.pid_min
        return output

    def update(self, measured_value):
        error = self.expected_value - measured_value
        integral = self.integral + error

        # Calculate the output signal
        output_proportional = self.kp * error
        output_integral = (1.0/self.ki) * integral
        output = self.within_min_max(output_proportional + output_integral)

        # Check that no windup can occur, if windup dont integrate the error.
        if self.pid_min < output < self.pid_max and 35.0 < measured_value < 39:
            self.integral = integral

        self.f1.write("V:"+str(measured_value)
                      + ", E:"+str(error)
                      + ", I:"+str(self.integral)
                      + ", Up:"+str(output_proportional)
                      + ", Ui:"+str(output_integral)
                      + ", U:"+str(output)+"\n")
        self.f1.flush()
        logging.debug("TEMP: %s OUT: %s E: %s P: %s I: %s", str(measured_value), int(output), str(error),
                      int(output_proportional), int(output_integral))

        self.set_value(output)
        return int(output)