# -*- coding: utf-8 -*-
""" Description """

from RPLCD.i2c import CharLCD
from .time import Time
# from .log_info import LogInfo

lcd = CharLCD('PCF8574', address=0x27)
time_obj = Time()
# logging.log_info('Module: ' + 'PCF8574' + ' loaded')


def __write_row1(text):
    """ Description """
    lcd.cursor_pos = (0, 6)
    lcd.write_string(text)


def __write_row2(text):
    """ Description """
    lcd.cursor_pos = (1, 0)
    lcd.write_string(text)


def __write_time():
    system_time = time_obj.sync()
    if system_time is not None:
        lcd.cursor_pos = (0, 0)
        lcd.write_string(system_time)


def write_lcd(what, show):
    """ Description """

    if what == 'kapali':
        __write_row1(u'kapali')

    elif what == 'start':
        __write_row1(u'calisiyor')

    elif what == 'stop':
        __write_row1(u'duruyor')

    elif what == 'bobin':
        __write_row1(u'bobin')

    elif what == 'cozgu':
        __write_row1(u'cozgu')

    elif what == 'ariza':
        __write_row1(u'ariza')

    elif what == 'ayar':
        __write_row1(u'ayar')

    elif what == 'reset':
        __write_row2(u'Counter= ' + '0      ')

    elif what == 'counter':
        __write_row2(u'Counter= ' + str(show))


def sync_time():
    """ Description """
    __write_time()
