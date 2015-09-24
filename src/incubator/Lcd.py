__author__ = 'tobias'

import smbus
import time


class Lcd():
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x2c
        self.back_light_on(1)
        self.set_contrast(150)

    def update(self, temp, day, pid, roll, humidity):
        try:
            self.clear()
            self.message("Temp: " + str(round(temp, 1)) + "  Dag: " + str(day) + "\n")
            self.message("PID : " + str(pid) + "/400\n")
            self.message("Turn: " + str(roll) + "\n")
            self.message("Humi: " + str(humidity))
        except:
            None

    def clear(self):
        self.bus.write_byte_data(self.address, 0xfe, 0x58)

    def blink_on(self):
        self.bus.write_byte_data(self.address, 0xfe, 83)

    def blink_on(self):
        self.bus.write_byte_data(self.address, 0xfe, 84)

    def set_contrast(self, contrast):
        self.bus.write_byte_data(self.address, 0xfe, ord('P'))
        self.bus.write_byte(self.address, contrast)

    def newline(self):
        self.bus.write_byte(self.address, 10)

    def back_light_on(self, minutes):
        self.bus.write_byte_data(self.address, 0xfe, 66)
        self.bus.write_byte(self.address, minutes)

    def send_command(self, data):
        self.bus.write_byte_data(self.address, 0xfe, data)

    def back_light_off(self):
        self.send_command(70)

    def message(self, text):
        """Write text to display.  Note that text can include newlines."""
        line = 0
        # Iterate through each character.
        for char in text:
            # Advance to next line if character is a new line.
            if char == '\n':
                self.newline()

            # line += 1
            # Move to left or right side depending on text direction.
            # col = 0 if self.displaymode & LCD_ENTRYLEFT > 0 else self._cols-1
            # self.set_cursor(col, line)
            # Write the character to the display.
            else:
                self.bus.write_byte(self.address, ord(char))