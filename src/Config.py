__author__ = 'tobias'
# coding=UTF-8


class Config:

    def __init__(self):
        self.config_file = 'incubator.properties'
        self.temp = 37.5
        self.day = None
        self.roll_interval = None
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

    def save(self):
        f = open(self.config_file, 'w')
        f.write("temp="+self.temp+"\n")
        f.write("day="+str(self.day)+"\n")
        f.write("roll_interval="+str(self.roll_interval)+"\n")
        f.close()