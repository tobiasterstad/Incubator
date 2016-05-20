__author__ = 'tobias'

import logging
import threading
import time
from htu21d import HTU21D


class Ventilation(threading.Thread):

    def __init__(self, q):

        self.q = q

        self.integral = 0
        self.expected_value = 0.0

        self.kp = 150
        self.ki = 1.0

        self.pid_max = 4095
        self.pid_min = 900

        self._running = True

        self.humidity = 50

        self.state = None
        self.output_level = None

        threading.Thread.__init__(self)

    def run(self):
        logging.info("Starting Ventilation")
        while self._running:
            if self.state is not None:
                humidity = self.state.get_humidity()
                temp = self.state.get_temp2()

                if humidity > 0 and self.humidity - 40 < humidity < self.humidity + 40:
                    self.humidity = humidity

                self.output_level = self.update(self.humidity)

                logging.debug("Humidity: {0}% RH, Level: {1}, Temp: {2}".format(self.humidity, self.output_level, temp))
                self.q.put_nowait("15:{0}".format(self.output_level))

            time.sleep(10)

        logging.info("Stopping Ventilation done")

    def stop(self):
        self._running = False

    def set_state(self, state):
        self.state = state

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
        if self.pid_min < output < self.pid_max:
            self.integral = integral

        logging.info("Ventilation: {0} OUT: {1} E: {2} P: {3} I: {4}"
                     .format(measured_value, output, error, output_proportional, output_integral))

        return int(output)

    def get_ki(self):
        return self.ki

    def get_output_level(self):
        if self.output_level is None:
            return 0

        return self.output_level