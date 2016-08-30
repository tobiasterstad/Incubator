__author__ = 'tobias'

import logging
import threading
import time
import json

from flask import Flask, request, render_template

app = Flask(__name__)

temp = 0.0
state = None
config = None
incubator = None


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

@app.route('/data')
def show_data():
    global temp
    global state
    return json.dump(state)


@app.route("/shutdown")
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "shutdown server"


@app.route("/humidity/<humidity>")
def set_humidity(humidity):
    global incubator
    humidity = int(humidity)
    if humidity < 40 or humidity > 80:
        raise Exception("humidity must be between 40 and 80")

    logging.info("Change humidity to {0}".format(humidity))
    incubator.set_humidity(humidity)
    return "humidity set"


class Web(threading.Thread):

    def __init__(self, incubator2):
        print("Start WS")
        self._running = False
        threading.Thread.__init__(self)
        self.incubator = incubator2
        global incubator
        incubator = incubator2

    def run(self):
        logging.info("Starting Web")
        self._running = True

        global app
        app.run(host='0.0.0.0', port=4000)
        logging.info("Shutdown")
        self._running = False
        # self.incubator.signal_term_handler(None, None)
        self.incubator.shutdown()

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

