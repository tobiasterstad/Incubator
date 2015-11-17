__author__ = 'tobias'


import os


class Dimmer:
    def __init__(self, debug):
        self.debug = debug

    def dim(self, pid):
        if self.debug == 1:
            pass
        else:
            os.system("/home/pi/dim.sh " + str(pid))
