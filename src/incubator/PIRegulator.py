__author__ = 'tobias'

import logging


class PIRegulator:

    def __init__(self, kp, ki, normal):
        self.integral = 0
        self.expected_value = 0.0
        self.kp = kp
        self.ki = ki

        self.pid_max = 400
        self.pid_min = 0
        self.f1 = open('/var/www/pid.php', 'w+')
        self.normal = normal

    def set_point(self, value=1.0):
        self.expected_value = value

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
        if self.pid_min < output < self.pid_max and 36.0 < measured_value < 39:
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
        return int(output)

    def get_ki(self):
        return self.ki
