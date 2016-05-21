__author__ = 'tobias'
# coding=UTF-8


class Config:

    def __init__(self):
        self.config_file = 'incubator.properties'
        self.temp = 37.5
        self.normal = 100
        self.day = None
        self.roll_interval = None
        self.humidity = 45
        self.k = 100.0
        self.i = 1.0
        self.token = ''
        self.user_key = ''
        self.debug = False
        self.reload()

    def reload(self):
        f = open(self.config_file, 'r')
        for line in f:
            x = line.split('=')

            if x[0] == 'temp':
                self.temp = x[1].strip()

            if x[0] == 'day':
                self.day = x[1].strip()

            if x[0] == 'roll_interval':
                self.roll_interval = x[1].strip()

            if x[0] == 'normal':
                self.normal = x[1].strip()

            if x[0] == 'humidity':
                self.humidity = x[1].strip()

            if x[0] == 'k':
                self.k = x[1].strip()

            if x[0] == 'i':
                self.i = x[1].strip()

            if x[0] == 'token':
                self.token = x[1].strip()

            if x[0] == 'user_key':
                self.user_key = x[1].strip()

            if x[0] == 'debug':
                if x[1].strip() == 'True':
                    self.debug = True
                else:
                    self.debug = False
        f.close()

    def get_temp(self):
        return float(self.temp)

    def get_day(self):
        if self.day is None or self.day == "":
            return 1
        else:
            return int(self.day)

    def get_roll_intervall(self):
        return int(self.roll_interval)

    def set_day(self, day):
        self.day = day

    def get_humidity(self):
        return int(self.humidity)

    def set_humidity(self, humidity):
        self.humidity = humidity

    def get_k(self):
        return round(float(self.k), 1)

    def get_i(self):
        return round(float(self.i), 1)

    def save(self):
        f = open(self.config_file, 'w')
        f.write("temp="+str(self.temp)+"\n")
        f.write("day="+str(self.day)+"\n")
        f.write("roll_interval="+str(self.roll_interval)+"\n")
        f.write("humidity="+str(self.humidity)+"\n")
        f.write("k="+str(self.k)+"\n")
        f.write("i="+str(self.i)+"\n")
        f.write("token={0}\n".format(self.token))
        f.write("user_key={0}\n".format(self.user_key))
        f.write("debug={0}\n".format(self.debug))
        f.close()

    def get_token(self):
        return self.token

    def get_user_key(self):
        return self.user_key

    def get_debug(self):
        return self.debug