__author__ = 'tobias'

#The recipe gives simple implementation of a Discrete Proportional-Integral-Derivative (PID) controller. PID controller gives output value for error between desired reference input and measurement feedback to minimize error value.
#More information: http://en.wikipedia.org/wiki/PID_controller
#
#cnr437@gmail.com
#
#######	Example	#########
#
#p=PID(3.0,0.4,1.2)
#p.setPoint(5.0)
#while True:
#     pid = p.update(measurement_value)
#
#


class PID:
    """
    Discrete PID control
    """

    def __init__(self, p=2.0, i=0.0, d=1.0, derivator=0, integrator=0, integrator_max=500, integrator_min=-500):

        self.kp = p
        self.ki = i
        self.kd = d
        self.derivator = derivator
        self.integrator = integrator
        self.integrator_max = integrator_max
        self.integrator_min = integrator_min

        self.set_point = 0.0
        self.error = 0.0

        self.p_value = 0.0
        self.d_value = 0.0
        self.i_value = 0.0

    def update(self, current_value):
        """
        Calculate PID output value for given reference input and feedback
        """

        self.error = self.set_point - current_value

        self.p_value = self.kp * self.error
        self.d_value = self.kd * (self.error - self.derivator)
        self.derivator = self.error

        self.integrator = self.integrator + self.error

        if self.integrator > self.integrator_max:
            self.integrator = self.integrator_max
        elif self.integrator < self.integrator_min:
            self.integrator = self.integrator_min

        self.i_value = self.integrator * self.ki

        #print(self.P_value, self.I_value, self.D_value)

        pid = self.p_value + self.i_value + self.d_value
        print(current_value, int(pid), int(self.p_value), int(self.i_value), int(self.d_value))

        if current_value > 38.5:
            pid = self.p_value + self.i_value + self.d_value + (self.error * 80)

        if pid > 255:
            pid = 255
        elif pid < 0:
            pid = 0

        return int(pid)

    def setPoint(self,set_point):
        """
        Initilize the setpoint of PID
        """
        self.set_point = set_point
        self.integrator = 0
        self.derivator = 0

    def setIntegrator(self, integrator):
        self.integrator = integrator

    def setDerivator(self, Derivator):
        self.derivator = Derivator

    def setKp(self,P):
        self.kp=P

    def setKi(self,I):
        self.ki=I

    def setKd(self,D):
        self.kd=D

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.integrator

    def getDerivator(self):
        return self.derivator


# measurement_value=20
#
# p=PID(3.0,0.4,1.2)
# p.setPoint(38)
# while True:
#     pid = p.update(measurement_value)
#     print measurement_value, pid
#     time.sleep(1)
