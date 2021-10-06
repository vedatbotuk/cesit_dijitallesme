#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

import RPi.GPIO as GPIO


class KeyPad:
    GPIO.setmode(GPIO.BCM)

    def __init__(self, rows_pins=None, cols_pins=None):

        if cols_pins is None:
            cols_pins = [12, 16, 20, 21]
        if rows_pins is None:
            rows_pins = [18, 23, 24, 25]

        self.rows_pins = rows_pins
        self.cols_pins = cols_pins

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(rows_pins[0], GPIO.OUT)
        GPIO.setup(rows_pins[1], GPIO.OUT)
        GPIO.setup(rows_pins[2], GPIO.OUT)
        GPIO.setup(rows_pins[3], GPIO.OUT)

        GPIO.setup(cols_pins[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(cols_pins[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(cols_pins[2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(cols_pins[3], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def __read_line(self, line, characters):
        pressed_button = None
        GPIO.output(line, GPIO.HIGH)
        if GPIO.input(self.cols_pins[0]) == 1:
            pressed_button = characters[0]
        if GPIO.input(self.cols_pins[1]) == 1:
            pressed_button = characters[1]
        if GPIO.input(self.cols_pins[2]) == 1:
            pressed_button = characters[2]
        if GPIO.input(self.cols_pins[3]) == 1:
            pressed_button = characters[3]
        GPIO.output(line, GPIO.LOW)
        return pressed_button

    def check_button(self):
        get_key0 = self.__read_line(self.rows_pins[0], ["1", "2", "3", "A"])
        get_key1 = self.__read_line(self.rows_pins[1], ["4", "5", "6", "B"])
        get_key2 = self.__read_line(self.rows_pins[2], ["7", "8", "9", "C"])
        get_key3 = self.__read_line(self.rows_pins[3], ["*", "0", "#", "D"])

        if get_key0 is not None:
            return get_key0

        elif get_key1 is not None:
            return get_key1

        elif get_key2 is not None:
            return get_key2

        elif get_key3 is not None:
            return get_key3
        else:
            return ''
