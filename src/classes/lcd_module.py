#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

from RPLCD.i2c import CharLCD
from .json_funcs import get_setup
from .time import Time
from .log_info import LogInfo

config_json = get_setup()
logging = LogInfo(config_json['main']['log'],
                  config_json['main']['log_level'],
                  config_json['main']['log_path'])

class LcdModule:
    """ Description """

    def __init__(self, model='PCF8574', address=0x27):

        self.text = ''
        self.line1 = ''
        self.line2 = ''
        self.model = model
        self.address = address
        self.time_obj = Time()
        self.system_time = self.time_obj.sync()

        # cols is because of linebreak and line return 17. Like bellow.
        # self.text = str(self.__sync_time()) + self.line1 + '\n\r' + self.line2
        try:
            self.lcd = CharLCD(self.model,
                               self.address,
                               port=1,
                               cols=17,
                               rows=2,
                               dotsize=8,
                               charmap='A02',
                               auto_linebreaks=False,
                               backlight_enabled=True)
        except Exception as e:
            logging.log_info(e)

        logging.log_info('Module: ' + self.model + ' loaded')

    def refresh_lcd(self, what, state):
        """ Description """
        # self.line1 =

        if what == 'kapali':
            self.line1 = '     ' + u'kapali'
            self.line2 = u'Counter=' + str(state)

        elif what == 'start':
            self.line1 = '  ' + u'calisiyor'
            self.line2 = u'Counter=' + str(state)

        elif what == 'stop':
            self.line1 = '    ' + u'duruyor'
            self.line2 = u'Counter=' + str(state)

        elif what == 'bobin':
            self.line1 = '      ' + u'bobin'
            self.line2 = u'Counter=' + str(state)

        elif what == 'cozgu':
            self.line1 = '      ' + u'cozgu'
            self.line2 = u'Counter=' + str(state)

        elif what == 'ariza':
            self.line1 = '      ' + u'ariza'
            self.line2 = u'Counter=' + str(state)

        elif what == 'ayar':
            self.line1 = '       ' + u'ayar'
            self.line2 = u'Counter=' + str(state)

        elif what == 'start_system':
            self.line1 = '     ' + u'kapali'
            self.line2 = u'...'

        if state == 0:
            self.line2 = u'Counter=' + '0       '
        else:
            self.line2 = u'Counter=' + str(state)

        text_old = self.text
        self.text = str(self.__sync_time()) + self.line1 + '\n\r' + self.line2
        if text_old != self.text:
            try:
                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(self.text)
            except Exception as e:
                logging.log_info(e)

    def __sync_time(self):
        """ Description """
        self.system_time = self.time_obj.sync()
        return self.system_time

    def lcd_close(self):
        """ Description """
        self.lcd.close(clear=True)
