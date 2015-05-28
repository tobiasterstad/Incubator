__author__ = 'tobias'
# coding=UTF-8

from PIRegulator import PIRegulator
from Roller import Roller
from TempSensor import TempSensor
from DimmerServo import DimmerServo
from datetime import *
from Config import Config
from Web import *

import time
import sys
import logging


class Incubator:
    def __init__(self):
        print "Init incubator."
        config = Config()
        day_tmp = config.get_day()

        if day_tmp != 1:
            self.start_time = datetime.today() - timedelta(days=day_tmp - 1)
            self.roll_time = datetime.today()
        else:
            self.start_time = datetime.today()
            self.roll_time = datetime.today()

    # Get the number of days since start
    def get_days_from_start(self):
        diff = datetime.today() - self.start_time
        return diff.days + 1

    def main(self):
        logging.basicConfig(level=logging.INFO)

        logging.info("Incubator started " + self.start_time.strftime('%Y-%m-%d %H:%M:%S'))

        config = Config()

        p = PIRegulator(200, 5)
        p.set_point(config.get_temp())

        roller = Roller()
        web = Web()

        temp_sensor = TempSensor()
        dimmer = DimmerServo()
        i = 0
        while True:
            temp = temp_sensor.read_temp()
            pid = p.update(temp)
            dimmer.dim(pid)

            if i >= 5:
                # Set new temp from config file
                config.reload()
                p.set_point(config.get_temp())

                day = self.get_days_from_start()

                if roller.is_time_to_role(day, config):
                    roller.roll()

                if config.get_day() != day:
                    config.set_day(day)
                    config.save()

                time_str = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                logging.info(time_str + ", " + str(config.get_temp()) + ", " + str(temp) + ", " + str(pid) + ", "
                             + str(day) + ", " + str(roller.get_minutes_from_last_roll()))

                # update web page
                web.update(time_str, str(temp), str(pid))

                i = 0
            else:
                i += 1
                # print str(pid)

            sys.stdout.flush()
            time.sleep(1)


incubator = Incubator()
incubator.main()
