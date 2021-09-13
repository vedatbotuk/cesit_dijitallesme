#!/usr/bin/python3
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

        self.lcd = CharLCD(self.model,
                           self.address,
                           port=1,
                           cols=16,
                           rows=2,
                           dotsize=8,
                           charmap='A02',
                           auto_linebreaks=True,
                           backlight_enabled=True)
        # self.lcd.cursor_mode('hide')

        logging.log_info('Module: ' + self.model + ' loaded')

    # def write_lcd(self, what, show):
    # 
    #     if what == 'kapali':
    #         self.lcd.cursor_pos = (0, 0)
    #         self.lcd.write_string(self.system_time + '    ' + u'kapali')
    # 
    #     elif what == 'start':
    #         self.lcd.cursor_pos = (0, 0)
    #         self.lcd.write_string(self.system_time + ' ' + u'calisiyor')
    # 
    #     elif what == 'stop':
    #         self.lcd.cursor_pos = (0, 0)
    #         self.lcd.write_string(self.system_time + '   ' + u'duruyor')
    # 
    #     elif what == 'bobin':
    #         self.lcd.cursor_pos = (0, 0)
    #         self.lcd.write_string(self.system_time + '     ' + u'bobin')
    # 
    #     elif what == 'cozgu':
    #         self.lcd.cursor_pos = (0, 0)
    #         self.lcd.write_string(self.system_time + '     ' + u'cozgu')
    # 
    #     elif what == 'ariza':
    #         self.lcd.cursor_pos = (0, 0)
    #         self.lcd.write_string(self.system_time + '     ' + u'ariza')
    # 
    #     elif what == 'ayar':
    #         self.lcd.cursor_pos = (0, 0)
    #         self.lcd.write_string(self.system_time + '      ' + u'ayar')
    # 
    #     elif what == 'reset':
    #         self.lcd.cursor_pos = (1, 0)
    #         self.lcd.write_string(u'Counter= ' + '0      ')
    # 
    #     elif what == 'counter':
    #         self.lcd.cursor_pos = (1, 0)
    #         self.lcd.write_string(u'Counter= ' + str(show))
        
    def refresh_lcd(self, what, counter):
        text_old = self.text
        self.text = str(self.__sync_time()) + str(what) + '\n\r' + u'Counter=' + str(counter)
        if text_old != self.text:
            self.lcd.write_string(self.text)

    def __sync_time(self):
        """ Description """
        self.system_time = self.time_obj.sync()
        return self.system_time

    def lcd_close(self):
        self.lcd.close(clear=True)
