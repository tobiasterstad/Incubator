__author__ = 'tobias'

from src.incubator.servopi.ABE_ServoPi import PWM


# 0 - 420      145/570
class DimmerServo:

    def __init__(self):
        # Initialise the PWM device using the default address,
        # change this value if you have bridged the address selection jumpers
        self.pwm = PWM(0x40)

        self.dimmer_max = 145  # Min pulse length out of 4096
        self.dimmer_min = 570  # Max pulse length out of 4096

        # Set PWM frequency to 50 Hz
        self.pwm.set_pwm_freq(50)
        self.pwm.output_enable()

    def dim(self, level):
        servo = level + 145

        if servo > self.dimmer_min:
            servo = self.dimmer_min
        elif servo < self.dimmer_max:
            servo = self.dimmer_max

        # print level
        self.pwm.set_pwm(15, 0, servo)
