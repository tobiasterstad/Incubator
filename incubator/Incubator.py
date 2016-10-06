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
import HttpSender


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

        self.config = Config()
        self._running = True

        if day_tmp != 1:
            self.start_time = datetime.today() - timedelta(days=day_tmp - 1)
            self.roll_time = datetime.today()
        else:
            self.start_time = datetime.today()
            self.roll_time = datetime.today()

    def set_humidity(self, humidity):
        self.config.set_humidity(humidity)
        self.config.save()

    def send_notification(self, message):
        try:
            token = self.config.get_token()
            user_key = self.config.get_user_key()

            pushover.init(token)
            pushover.Client(user_key).send_message(message, title="Incubator")
        except:
            logging.error("Failed to notify")

    def signal_term_handler(self, signal, frame):
        logging.debug("got SIGTERM")
        self.shutdown()

    # Get the number of days since start
    def get_days_from_start(self):
        diff = datetime.today() - self.start_time
        return diff.days + 1

    def log_incubator_state(self, config, state):
        data = {
            "ts": state.get_ts(),
            "temp1": state.get_temp1(),
            "temp2": state.get_temp2(),
            "set_temp": config.get_temp(),
            "heat pid": state.get_pid(),
            "day": state.get_day(),
            "humidity": state.get_humidity(),
            "humidity pid": state.get_humidity_level(),
            "roller": self.roller.get_minutes_from_last_roll()
        }

        logging.info(data)

        # logging.info(time_str + ", " + str(config.get_temp()) + ", " + str(temp) + ", " + str(pid) + ", "
        #              + str(day) + ", " + str(state.get_humidity()) + ", " + str(
        #     self.roller.get_minutes_from_last_roll()))

    def shutdown(self):
        self._running = False

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

    def get_humidity(self):
        hum = self.config.get_humidity()
        if hum == 0:
            if self.get_days_from_start() >= 0:
                hum = 30
            if self.get_days_from_start() >= 7:
                hum = 40
            if self.get_days_from_start() >= 14:
                hum = 50
            if self.get_days_from_start() >= 18:
                hum = 70
        return hum

    def main(self):
        logging.info("Incubator started... " + self.start_time.strftime('%Y-%m-%d %H:%M:%S'))
        self.send_notification("Incubator started")

        self.ssr.set_point(self.config.get_temp())

        # Start roller
        self.roller.set_day(self.config.get_day())
        self.roller.start()

        web = Web.Web(self)
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

        http_sender = HttpSender.HttpSender()

        while self._running:
            state.update_ts()
            state.set_temp1(temp_sensor.read_temp())

            pid = self.ssr.update(state.get_temp1())
            state.set_pid(pid)

            #if state.temp1 > 38.5:
            #    self.send_notification("High temp alert, {} gr".format(state.temp1))

            if i >= 10:
                # Read humidity and temp each 10 seconds
                try:
                    state.set_temp2(htu21d.read_temperature())
                    state.set_humidity(htu21d.read_humidity())
                except:
                    self.send_notification("Failed to read htu21d")

                self.ventilation.set_state(state)
                state.set_humidity_level(self.ventilation.get_output_level())

                http_sender.send("A123", state)

            if i >= 30:
                # Set new temp from config file
                self.config.reload()
                self.ssr.set_point(self.config.get_temp())
                self.ssr.set_k(self.config.get_k())
                self.ssr.set_i(self.config.get_i())

                self.ventilation.set_point(self.get_humidity())

                state.set_day(self.get_days_from_start())

                if self.config.get_day() != state.get_day():
                    self.config.set_day(state.get_day())
                    self.config.save()
                    self.roller.set_day(state.get_day())

                self.log_incubator_state(self.config, state)

                # update web page
                web.update(state, self.config)

                i = 0
            else:
                i += 1

            lcd.update(state, self.roller.get_minutes_from_last_roll())
            sys.stdout.flush()
            time.sleep(1)

        self.shutdown()


if __name__ == '__main__':
    logging.basicConfig(filename='incubator.log', format='%(asctime)s %(levelname)s : %(name)s : %(message)s',
                        level=logging.DEBUG)

    incubator = Incubator()

    # Add signal handler
    signal.signal(signal.SIGTERM, incubator.signal_term_handler)
    signal.signal(signal.SIGHUP, incubator.signal_term_handler)

    # Run incubator
    incubator.main()
