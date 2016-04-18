__author__ = 'tobias'
# coding=UTF-8

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
        logging.debug("Init incubator.")
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
        logging.debug("got SIGTERM")
        self.roller.stop()
        self.ssr.stop()
        self.ventilation.stop()
        self.pwm_controller.stop()
        logging.info("Stopped Incubator")
        sys.exit(0)

    # Get the number of days since start
    def get_days_from_start(self):
        diff = datetime.today() - self.start_time
        return diff.days + 1

    def main(self):
        logging.info("Incubator started... " + self.start_time.strftime('%Y-%m-%d %H:%M:%S'))

        config = Config()
        self.ssr.set_point(config.get_temp())

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
            pid = self.ssr.update(temp)

            if i >= 30:
                # Set new temp from config file
                config.reload()
                self.ssr.set_point(config.get_temp())
                self.ssr.set_k(config.get_k())
                self.ssr.set_i(config.get_i())

                self.ventilation.set_point(config.get_humidity())

                day = self.get_days_from_start()

                if config.get_day() != day:
                    config.set_day(day)
                    config.save()
                    self.roller.set_day(day)

                time_str = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                logging.info(time_str + ", " + str(config.get_temp()) + ", " + str(temp) + ", " + str(pid) + ", "
                             + str(day) + ", " + str(self.ventilation.get_humidity()) + ", " + str(self.roller.get_minutes_from_last_roll()))

                # update web page
                web.update(time_str, str(temp), str(pid))

                i = 0
            else:
                i += 1

            lcd.update(temp, day, pid, self.roller.get_minutes_from_last_roll(), self.ventilation.get_humidity())
            sys.stdout.flush()
            time.sleep(1)

        # Stop all services
        self.roller.stop()
        self.ssr.stop()
        self.ventilation.stop()
        self.pwm_controller.stop()
        self.q.put("exit")

        self.roller.join()
        self.ssr.join()
        self.ventilation.join()
        self.pwm_controller.join()
        # self.io_handler.stop()


if __name__ == '__main__':
    logging.basicConfig(filename='incubator.log', format='%(asctime)s %(levelname)s : %(name)s : %(message)s',
                        level=logging.DEBUG)

    incubator = Incubator()

    # Add signal handler
    signal.signal(signal.SIGTERM, incubator.signal_term_handler)

    # Run incubator
    incubator.main()
