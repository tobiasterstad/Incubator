__author__ = 'tobias'

from ventilation.htu21d import HTU21D
from TempSensor import TempSensor
import devmocks
import Config


config = Config.Config()


def create_humidity_sensor():
    if config.get_debug():
        return devmocks.HTU21D()
    else:
        return HTU21D()


def create_temp_sensor():
    if config.get_debug():
        return devmocks.TempSensor()
    else:
        return TempSensor()