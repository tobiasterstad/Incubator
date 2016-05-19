__author__ = 'tobias'

import logging
import threading
import time
from htu21d import HTU21D


class Ventilation(threading.Thread):

    def __init__(self, q):

        # self.pwm = PWM(smbus.SMBus(1), 0x60)
        # self.pwm.set_pwm_freq(50)
        # self.pwm.output_enable()

        self.q = q

        self.integral = 0
        self.expected_value = 0.0

        self.kp = 150
        self.ki = 1.0

        self.pid_max = 4095
        self.pid_min = 2000

        self._running = True

        self.humidity = 50

        init_ok = False
        while not init_ok:
            try:
                self.htu21d = HTU21D()
                init_ok = True
            except:
                logging.error("Failed to init humidity sensor")
                init_ok = False
                time.sleep(1)

        threading.Thread.__init__(self)

    def run(self):
        logging.info("Starting Ventilation")
        while self._running:
            try:
                humidity = self.htu21d.read_humidity()
                temp = self.htu21d.read_temperature()

                if humidity > 0 and self.humidity - 40 < humidity < self.humidity + 40:
                    self.humidity = humidity

                level = self.update(self.humidity)

                logging.debug("Humidity: {0}% RH, Level: {1}, Temp: {2}".format(self.humidity, level, temp))
                self.q.put_nowait("15:{0}".format(level))
            except:
                logging.debug("failed to read humidity")

            time.sleep(10)

        logging.info("Stopping Ventilation done")

    def stop(self):
        self._running = False

    def set_point(self, value=1.0):
        if self.expected_value != value:
            logging.debug("Change ventilation set point {}".format(value))
        self.expected_value = value

    def within_min_max(self, output):
        if output > self.pid_max:
            output = self.pid_max
        if output < self.pid_min:
            output = self.pid_min
        return output

    def update(self, measured_value):
        error = measured_value - self.expected_value
        integral = self.integral + error

        # Calculate the output signal
        output_proportional = self.kp * error
        output_integral = (1.0/self.ki) * integral
        output = self.within_min_max(output_proportional + output_integral)

        # Check that no windup can occur, if windup dont integrate the error.
        if self.pid_min <= output <= self.pid_max:
            self.integral = integral

        logging.info("Ventilation: {0} OUT: {1} E: {2} P: {3} I: {4}"
                     .format(measured_value, output, error, output_proportional, output_integral))

        return int(output)

    def get_ki(self):
        return self.ki

    def get_humidity(self):
        return int(self.humidity)

    def get_temp(self):
        return round(self.htu21d.read_temperature(), 1)