# -*- coding: utf-8 -*-
""" Description """

from RPLCD.i2c import CharLCD
from .time import Time
# from .log_info import LogInfo

lcd = CharLCD('PCF8574', address=0x27)
time_obj = Time()
# logging.log_info('Module: ' + 'PCF8574' + ' loaded')


# def __write_row1(text):
#     """ Description """
#     lcd.cursor_pos = (0, 0)
#     lcd.write_string(text)
#
#
# def __write_row2(text):
#     """ Description """
#     lcd.cursor_pos = (1, 0)
#     lcd.write_string(text)


def __write_time():
    system_time = time_obj.sync()
    if system_time is not None:
        lcd.cursor_pos = (0, 0)
        lcd.write_string(system_time)


def write_lcd(what, show):
    # date_wl = get_date_time('basic')
    # global system_time

    if what == 'kapali':
        lcd.cursor_pos = (0, 0)
        lcd.write_string('     ' + '    ' + u'kapali')

    elif what == 'start':
        lcd.cursor_pos = (0, 0)
        lcd.write_string('     ' + ' ' + u'calisiyor')

    elif what == 'stop':
        lcd.cursor_pos = (0, 0)
        lcd.write_string('     ' + '   ' + u'duruyor')

    elif what == 'bobin':
        lcd.cursor_pos = (0, 0)
        lcd.write_string('     ' + '     ' + u'bobin')

    elif what == 'cozgu':
        lcd.cursor_pos = (0, 0)
        lcd.write_string('     ' + '     ' + u'cozgu')

    elif what == 'ariza':
        lcd.cursor_pos = (0, 0)
        lcd.write_string('     ' + '     ' + u'ariza')

    elif what == 'ayar':
        lcd.cursor_pos = (0, 0)
        lcd.write_string('     ' + '      ' + u'ayar')

    elif what == 'reset':
        lcd.cursor_pos = (1, 0)
        lcd.write_string(u'Counter= ' + '0      ')

    elif what == 'counter':
        lcd.cursor_pos = (1, 0)
        lcd.write_string(u'Counter= ' + str(show))

def sync_time():
    """ Description """
    __write_time()
