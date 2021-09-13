# -*- coding: utf-8 -*-
""" Description """

from RPLCD.i2c import CharLCD
from .json_funcs import get_setup
from .time import Time
from .log_info import LogInfo

class LcdModule:
    """ Description """

    def __init__(self, model='PCF8574', address=0x27):

        config_json = get_setup()
        logging = LogInfo(config_json['main']['log'],
                          config_json['main']['log_level'],
                          config_json['main']['log_path'])

        self.text = ''
        self.model = model
        self.address = address
        self.time_obj = Time()
        self.system_time = self.time_obj.sync()

        self.lcd = CharLCD(model, address)

        logging.log_info('Module: ' + self.model + ' loaded')

    def __write_row1(self, text):
        """ Description """
        self.lcd.cursor_pos = (0, 6)
        self.lcd.write_string(text)

    def __write_row2(self, text):
        """ Description """
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(text)

    def __write_time(self):
        self.system_time = self.time_obj.sync()
        if self.system_time:
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string(self.system_time)

    def write_lcd(self, what, show):
        """ Description """

        if what == 'kapali':
            self.__write_row1(u'kapali')

        elif what == 'start':
            self.__write_row1(u'calisiyor')

        elif what == 'stop':
            self.__write_row1(u'duruyor')

        elif what == 'bobin':
            self.__write_row1(u'bobin')

        elif what == 'cozgu':
            self.__write_row1(u'cozgu')

        elif what == 'ariza':
            self.__write_row1(u'ariza')

        elif what == 'ayar':
            self.__write_row1(u'ayar')

        elif what == 'reset':
            self.__write_row2(u'Counter= ' + '0      ')

        elif what == 'counter':
            self.__write_row2(u'Counter= ' + str(show))

    def sync_time(self):
        """ Description """
        self.__write_time()
