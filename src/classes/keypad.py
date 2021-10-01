#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

import RPi.GPIO as GPIO
from time import sleep


class KeyPad:
    GPIO.setmode(GPIO.BCM)

    def __init__(self, rows_pins=None, cols_pins=None):

        if cols_pins is None:
            cols_pins = [12, 16, 20, 21]
        if rows_pins is None:
            rows_pins = [18, 23, 24, 25]

        self.rows_pins = rows_pins
        self.cols_pins = cols_pins

        self.matrix = [["1", "2", "3", "A"],
                       ["4", "5", "6", "B"],
                       ["7", "8", "9", "C"],
                       ["*", "0", "#", "D"]]

        for j in range(4):
            GPIO.setup(self.cols_pins[j], GPIO.OUT)
            GPIO.output(self.cols_pins[j], 1)
            GPIO.setup(self.rows_pins[j], GPIO.IN,
                       pull_up_down=GPIO.PUD_UP)

        self.buttons_input = None

    # def check_button(self, check_character):
    #     for j1 in range(4):
    #         GPIO.output(self.cols_pins[j1], 0)
    #         for ii in range(4):
    #             if GPIO.input(self.rows_pins[ii]) == 0:
    #                 self.buttons_input = self.matrix[ii][j1]
    #                 while GPIO.input(self.rows_pins[ii]) == 0:
    #                     pass
    #                 # if self.buttons_input == check_character:
    #                 #     return True
    #         GPIO.output(self.cols_pins[j1], 1)
    #
    #     if self.buttons_input == check_character:
    #         return True

    def check_button(self):
        self.buttons_input = ''
        for jj in range(4):
            GPIO.output(self.cols_pins[jj], 0)
            for ii in range(4):
                if GPIO.input(self.rows_pins[ii]) == 0:
                    self.buttons_input = self.matrix[ii][jj]
                    while GPIO.input(self.rows_pins[ii]) == 0:
                        pass
                    # if buttons_input is not None or not 'None':
                    #     return buttons_input
                    # else:
                    #     return ''
            GPIO.output(self.cols_pins[jj], 1)

        return self.buttons_input
