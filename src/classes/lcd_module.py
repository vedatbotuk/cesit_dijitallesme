#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

from RPLCD.i2c import CharLCD
from .json_funcs import get_setup
from .time import Time
from .log_info import LogInfo


# def write_lcd(what, show):
#
#     if what == 'kapali':
#         # self.lcd.cursor_pos = (0, 0)
#         # self.lcd.write_string(self.system_time + '    ' + u'kapali')
#         return '   ' + u'kapali'
#
#     elif what == 'start':
#         # self.lcd.cursor_pos = (0, 0)
#         # self.lcd.write_string(self.system_time + ' ' + u'calisiyor')
#         return u'calisiyor'
#
#     elif what == 'stop':
#         # self.lcd.cursor_pos = (0, 0)
#         # self.lcd.write_string(self.system_time + '   ' + u'duruyor')
#         return '  ' + u'duruyor'
#
#     elif what == 'bobin':
#         # self.lcd.cursor_pos = (0, 0)
#         # self.lcd.write_string(self.system_time + '     ' + u'bobin')
#         return '    ' + u'bobin'
#
#     elif what == 'cozgu':
#         # self.lcd.cursor_pos = (0, 0)
#         # self.lcd.write_string(self.system_time + '     ' + u'cozgu')
#         return '    ' + u'cozgu'
#
#     elif what == 'ariza':
#         # self.lcd.cursor_pos = (0, 0)
#         # self.lcd.write_string(self.system_time + '     ' + u'ariza')
#         return '    ' + u'ariza'
#
#     elif what == 'ayar':
#         # self.lcd.cursor_pos = (0, 0)
#         # self.lcd.write_string(self.system_time + '      ' + u'ayar')
#         return '     ' + u'ayar'
#
#     elif what == 'reset':
#         # self.lcd.cursor_pos = (1, 0)
#         # self.lcd.write_string(u'Counter= ' + '0      ')
#         return u'Counter=' + '0       '
#
#     elif what == 'counter':
#         # self.lcd.cursor_pos = (1, 0)
#         # self.lcd.write_string(u'Counter= ' + str(show))
#         print(u'Counter=' + str(show))
#         print(len(u'Counter=' + str(show)))
#         return u'Counter=' + str(show)


class LcdModule:
    """ Description """

    def __init__(self, model='PCF8574', address=0x27):

        config_json = get_setup()
        logging = LogInfo(config_json['main']['log'],
                          config_json['main']['log_level'],
                          config_json['main']['log_path'])

        self.text = ''
        self.line1 = ''
        self.line2 = ''
        self.model = model
        self.address = address
        self.time_obj = Time()
        self.system_time = self.time_obj.sync()

        # cols is because of linebreak and line return 17.
        self.lcd = CharLCD(self.model,
                           self.address,
                           port=1,
                           cols=17,
                           rows=2,
                           dotsize=8,
                           charmap='A00',
                           auto_linebreaks=False,
                           backlight_enabled=True)
        # self.lcd.cursor_mode('hide')

        logging.log_info('Module: ' + self.model + ' loaded')

    def refresh_lcd(self, what, state):
        # self.line1 =

        if what == 'kapali':
            # self.lcd.cursor_pos = (0, 0)
            # self.lcd.write_string(self.system_time + '    ' + u'kapali')
            self.line1 = '     ' + u'kapali'
            self.line2 = u'Counter=' + str(state)

        elif what == 'start':
            # self.lcd.cursor_pos = (0, 0)
            # self.lcd.write_string(self.system_time + ' ' + u'calisiyor')
            self.line1 = '  ' + u'calisiyor'
            self.line2 = u'Counter=' + str(state)

        elif what == 'stop':
            # self.lcd.cursor_pos = (0, 0)
            # self.lcd.write_string(self.system_time + '   ' + u'duruyor')
            self.line1 = '    ' + u'duruyor'
            self.line2 = u'Counter=' + str(state)

        elif what == 'bobin':
            # self.lcd.cursor_pos = (0, 0)
            # self.lcd.write_string(self.system_time + '     ' + u'bobin')
            self.line1 = '      ' + u'bobin'
            self.line2 = u'Counter=' + str(state)

        elif what == 'cozgu':
            # self.lcd.cursor_pos = (0, 0)
            # self.lcd.write_string(self.system_time + '     ' + u'cozgu')
            self.line1 = '      ' + u'cözgü'
            self.line2 = u'Counter=' + str(state)

        elif what == 'ariza':
            # self.lcd.cursor_pos = (0, 0)
            # self.lcd.write_string(self.system_time + '     ' + u'ariza')
            self.line1 = '      ' + u'ariza'
            self.line2 = u'Counter=' + str(state)

        elif what == 'ayar':
            # self.lcd.cursor_pos = (0, 0)
            # self.lcd.write_string(self.system_time + '      ' + u'ayar')
            self.line1 = '       ' + u'ayar'
            self.line2 = u'Counter=' + str(state)

        if state == 0 or state == '0':
            self.line2 = u'Counter=' + '0       '
        else:
            self.line2 = u'Counter=' + str(state)

        text_old = self.text
        self.text = str(self.__sync_time()) + self.line1 + '\n\r' + self.line2
        if text_old != self.text:
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string(self.text)

    # def refresh_lcd(self, what, counter):
    #     text_old = self.text
    #     # self.text = str(self.__sync_time()) + u' ' + str(what) + '\n\r' + u'Counter=' + str(counter)
    #     self.text = str(self.__sync_time()) + u' ' + write_lcd(what, None) + '\n\r' + write_lcd("counter", counter)
    #     # print(self.text)
    #     # print('lenght= ' + str(len(str(self.__sync_time()) + u' ' + str(write_lcd(what, None)))))
    #     if text_old != self.text:
    #         self.lcd.cursor_pos = (0, 0)
    #         self.lcd.write_string(self.text)

    def __sync_time(self):
        """ Description """
        self.system_time = self.time_obj.sync()
        return self.system_time

    def lcd_close(self):
        self.lcd.close(clear=True)
