__author__ = 'tobias'


class PID2:

    def __init__(self, kp, dt, ki, kd):
        self.previous_error = 0
        self.integral = 0
        self.error = 0
        self.expected_value = 0.0
        self.dt = dt
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.pid_max = 420
        self.pid_min = 0
        self.integral_max = self.pid_max / self.ki
        self.integral_min = -self.pid_max / self.ki

    def set_ki(self, ki):
        self.ki = ki
        self.integral_max = self.pid_max / self.ki
        self.integral_min = -self.pid_max / self.ki

    def set_point(self, value=1.0):
        self.expected_value = value

    @staticmethod
    def get_high_temp_protection(error, measured_value):
        high_temp_protection = 0
        if measured_value > 38:
            high_temp_protection = -100 * error
        return high_temp_protection

    def get_integral(self, error):
        integral = self.integral + error * self.dt
        if integral > self.integral_max:
            integral = self.integral_max
        if integral < self.integral_min:
            integral = self.integral_min
        return integral

    def get_derivative(self, error):
        derivative = (error - self.previous_error) / self.dt
        return derivative

    def within_min_max(self, output):
        if output > self.pid_max:
            output = self.pid_max
        if output < self.pid_min:
            output = self.pid_min
        return output

    def update(self, measured_value):

        # if measured_value >= 37.2:
        #     self.set_ki(1)
        #
        # if measured_value < 36.5:
        #     self.set_ki(8)

        error = self.expected_value - measured_value
        self.integral = self.get_integral(error)
        derivative = self.get_derivative(error)
        high_temp_protection = self.get_high_temp_protection(error, measured_value)

        output = self.kp*error + self.ki*self.integral + self.kd*derivative + high_temp_protection
        output = self.within_min_max(output)

        self.previous_error = error

        print(measured_value, int(output), int(self.kp*error), int(self.ki*self.integral), int(self.kd*derivative))
        return int(output)

    def get_ki(self):
        return self.ki