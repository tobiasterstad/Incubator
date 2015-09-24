__author__ = 'tobias'
# coding=UTF-8

from PIRegulator import PIRegulator
from Roller import Roller
from TempSensor import TempSensor
from datetime import *
from Config import Config
from Web import *
from Lcd import *
from dimmer.SSRRegulator import SSRRegulator
from iohandler.IoHandler import IoHandler
from ventilation.Ventilation import Ventilation

import signal
import time
import sys
import logging
from PWMController import PWMController
from Queue import Queue


class Incubator:
    def __init__(self):
        print "Init incubator."
        config = Config()
        day_tmp = config.get_day()

        q = Queue()
        self.q = q
        self.pwm_controller = PWMController(q)
        self.pwm_controller.start()

        self.roller = Roller(q, config.get_roll_intervall())
        self.ssr = SSRRegulator()
        # self.io_handler = IoHandler()

        self.ventilation = Ventilation(q)
        self.ventilation.set_point(40)
        self.ventilation.start()

        if day_tmp != 1:
            self.start_time = datetime.today() - timedelta(days=day_tmp - 1)
            self.roll_time = datetime.today()
        else:
            self.start_time = datetime.today()
            self.roll_time = datetime.today()

    def signal_term_handler(self, signal, frame):
        print "got SIGTERM"
        self.roller.stop()
        self.ssr.stop()
        self.ventilation.stop()
        print "stopped"
        sys.exit(0)

    # Get the number of days since start
    def get_days_from_start(self):
        diff = datetime.today() - self.start_time
        return diff.days + 1

    def main(self):
        logging.basicConfig(level=logging.INFO)

        logging.info("Incubator started... " + self.start_time.strftime('%Y-%m-%d %H:%M:%S'))

        config = Config()

        p = PIRegulator(100, 4.0, config.get_normal())
        p.set_point(config.get_temp())

        # Start roller

        self.roller.set_day(config.get_day())
        self.roller.start()

        web = Web()
        lcd = Lcd()

        temp_sensor = TempSensor()

        # Start SSR service
        self.ssr.set_value(0)
        self.ssr.start()

        # Start buttons and relays
        # self.io_handler.start()

        day = self.get_days_from_start()
        i = 0
        while True:
            temp = temp_sensor.read_temp()
            pid = p.update(temp)
            self.ssr.set_value(pid)

            if i >= 3:
                # Set new temp from config file
                config.reload()
                p.set_point(config.get_temp())
                self.ventilation.set_point(config.get_humidity())

                day = self.get_days_from_start()

                if config.get_day() != day:
                    config.set_day(day)
                    config.set_normal(pid)
                    config.save()
                    self.roller.set_day(day)

                time_str = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                logging.info(time_str + ", " + str(config.get_temp()) + ", " + str(temp) + ", " + str(pid) + ", "
                             + str(day) + ", " + str(self.ventilation.get_humidity()) + "," + str(self.roller.get_minutes_from_last_roll()))

                # update web page
                web.update(time_str, str(temp), str(pid))


                i = 0
            else:
                i += 1
                # print str(pid)

            lcd.update(temp, day, pid, self.roller.get_minutes_from_last_roll(), self.ventilation.get_humidity())
            sys.stdout.flush()
            time.sleep(10)

        # Stop all services
        self.roller.stop()
        self.ssr.stop()
        self.ventilation.stop()
        self.pwm_controller.stop()
        self.q.put("exit")
        # self.io_handler.stop()


incubator = Incubator()

# Add signal handler
signal.signal(signal.SIGTERM, incubator.signal_term_handler)

# Run incubator
incubator.main()
