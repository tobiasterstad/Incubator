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
        self.pid_min = 0

        self._running = True

        self.humidity = 50

        init_ok = False
        while not init_ok:
            try:
                self.htu21d = HTU21D()
                init_ok = True
            except:
                print("Failed to init humidity sensor")
                init_ok = False
                time.sleep(1)

        threading.Thread.__init__(self)

    def run(self):
        print "Starting Ventilation"
        while self._running:

            read_ok = False
            while not read_ok:
                try:
                    humidity = self.htu21d.read_humidity()
                    if humidity > 0 and self.humidity - 20 < humidity < self.humidity + 20:
                        read_ok = True
                        self.humidity = humidity
                except:
                    logging.debug("failed to read humidity")
                    read_ok = False
                    time.sleep(1)

            level = self.update(self.humidity)

            print("humidity", str(self.humidity))
            print("level", str(level))

            # self.pwm.set_pwm(1, on, off)
            self.q.put_nowait("15:"+str(level))
            time.sleep(10)

        print "Stopping Ventilation done"

    def stop(self):
        self._running = False
        print("Stopping Ventilation...")

    def set_point(self, value=1.0):
        if self.expected_value != value:
            print("Change ventilation set point" + str(value))
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

        logging.info("Ventilation: %s OUT: %s E: %s P: %s I: %s", str(measured_value), int(output), str(error),
                     int(output_proportional), int(output_integral))
        return int(output)

    def get_ki(self):
        return self.ki

    def get_humidity(self):
        return int(self.humidity)

    def get_temp(self):
        return round(self.htu21d.read_temperature(), 1)