__author__ = 'tobias'

import logging
import threading
import time

from flask import Flask
from flask import render_template

app = Flask(__name__)

temp = 0.0
state = None
config = None


@app.route('/')
def show_temp():
    global temp
    global state
    return render_template('temp.html',
                           temp1=state.get_temp1(),
                           temp2=state.get_temp2(),
                           humidity=state.get_humidity(),
                           ts=state.get_ts(),
                           day=state.get_day(),
                           pid=state.get_pid(),
                           set_temp=config.get_temp(),
                           set_humidity=config.get_humidity(),
                           humidity_level=state.get_humidity_level())


class Web(threading.Thread):

    def __init__(self):
        print("Start WS")
        self._running = False
        threading.Thread.__init__(self)

    def run(self):
        logging.info("Starting Web")
        self._running = True

        while self._running:
            global app
            app.run(host='0.0.0.0', port=4000)
            time.sleep(10)

    def update(self, new_state, new_config):
        logging.debug("Update web")
        global state, config
        state = new_state
        config = new_config

    def stop(self):
        print("Stop WS")
        global app
        app.stop()
        self._running = False

