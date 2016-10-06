__author__ = 'tobias'

import requests
import State


class HttpSender:

    def __init__(self):
        None

    def send(self, id, state):

        try:
            payload = {'id': id, 'day': state.day, 'humidity': state.humidity, 'humidity_level': state.humidity_level,
                       'pid': state.pid, 'temp1': state.temp1, 'temp2': state.temp2, 'ts': state.ts}
            # r = requests.post('http://10.100.0.13:123/data', data=state, timeout=1)
            r = requests.post('http://mini:8080/micro-1.0-SNAPSHOT/api/incubator/A123/values', json=payload, timeout=10)
            print(r)
        except requests.ConnectionError:
            print("error...")


if __name__ == '__main__':
    h = HttpSender()

    state = State.State()
    state.set_humidity(44.5)

    h.send("A123", state)