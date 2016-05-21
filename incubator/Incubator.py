__author__ = 'tobias'
# coding=UTF-8

from Roller import Roller

from datetime import *
from Config import Config
from Lcd import *
from SSRRegulator import SSRRegulator
# from iohandler.IoHandler import IoHandler
from ventilation.Ventilation import Ventilation
from State import State

from web import Web

import Resource
# import old.Web as OLDWeb

import signal
import time
import sys
import logging
from PWMController import PWMController
from Queue import Queue
import pushover


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

    def send_notification(self, message):
        pushover.init('aip68d2fg6k4xwcmewkvx7rm8z5r79')
        pushover.Client('u71gzv4guawn5k4cs24jnj726prkdh').send_message(message, title="Incubator")

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

    def log_incubator_state(self, config, state):
        time_str = state.get_ts()
        temp = state.get_temp1()
        pid = state.get_pid()
        day = state.get_day()

        data = {
            "ts": time_str,
            "temp": temp,
            "set_temp": config.get_temp(),
            "heat pid": pid,
            "day": day,
            "humidity": state.get_humidity(),
            "humidity pid": state.get_humidity_level(),
            "roller": self.roller.get_minutes_from_last_roll()
        }

        logging.info(data)

        # logging.info(time_str + ", " + str(config.get_temp()) + ", " + str(temp) + ", " + str(pid) + ", "
        #              + str(day) + ", " + str(state.get_humidity()) + ", " + str(
        #     self.roller.get_minutes_from_last_roll()))

    def main(self):
        logging.info("Incubator started... " + self.start_time.strftime('%Y-%m-%d %H:%M:%S'))

        self.send_notification("Incubator started")

        config = Config()
        self.ssr.set_point(config.get_temp())

        # Start roller
        self.roller.set_day(config.get_day())
        self.roller.start()

        web = Web.Web()
        web.start()
        lcd = Lcd()

        temp_sensor = Resource.create_temp_sensor()
        htu21d = Resource.create_humidity_sensor()

        # Start SSR service
        self.ssr.set_value(0)
        self.ssr.start()

        # Start buttons and relays
        # self.io_handler.start()

        i = 0
        state = State()
        state.set_day(self.get_days_from_start())
        while True:
            state.update_ts()
            state.set_temp1(temp_sensor.read_temp())

            pid = self.ssr.update(state.get_temp1())
            state.set_pid(pid)

            if state.temp1 > 37.8:
                self.send_notification("High temp alert, {} gr".format(state.temp1))

            if i >= 10:
                # Read humidity and temp each 10 seconds
                state.set_temp2(htu21d.read_temperature())
                state.set_humidity(htu21d.read_humidity())

                self.ventilation.set_state(state)
                state.set_humidity_level(self.ventilation.get_output_level())

            if i >= 30:
                # Set new temp from config file
                config.reload()
                self.ssr.set_point(config.get_temp())
                self.ssr.set_k(config.get_k())
                self.ssr.set_i(config.get_i())

                self.ventilation.set_point(config.get_humidity())

                state.set_day(self.get_days_from_start())

                if config.get_day() != state.get_day():
                    config.set_day(state.get_day())
                    config.save()
                    self.roller.set_day(state.get_day())

                self.log_incubator_state(config, state)

                # update web page
                web.update(state, config)

                i = 0
            else:
                i += 1

            lcd.update(state, self.roller.get_minutes_from_last_roll())
            sys.stdout.flush()
            time.sleep(1)

        # Stop all services
        self.roller.stop()
        self.ssr.stop()
        self.ventilation.stop()
        self.pwm_controller.stop()
        web.stop()
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
