#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

# imports
from RPi import GPIO
from .log_info import LogInfo
from .json_funcs import get_setup


def gpio_cleanup():
    """ Description """
    GPIO.cleanup()


class ButtonSwitch:
    """Library for quad 7-segment LED modules based on the TM1637 LED driver."""
    GPIO.setmode(GPIO.BCM)

    def __init__(self, gpio_no):
        """ Description """

        config_json = get_setup()

        self.logging = LogInfo(config_json['main']['log'],
                               config_json['main']['log_level'],
                               config_json['main']['log_path'])

        self.gpio_no = gpio_no
        self.sec_state = None
        self.btn_state = None

        GPIO.setup(self.gpio_no, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def add_callback(self, mode, callback):
        """ Test """

        if mode == 'falling':
            GPIO.add_event_detect(self.gpio_no, GPIO.FALLING, callback=callback, bouncetime=50)
        elif mode == 'both':
            GPIO.add_event_detect(self.gpio_no, GPIO.BOTH, callback=callback, bouncetime=50)
        elif mode == 'rising':
            GPIO.add_event_detect(self.gpio_no, GPIO.RISING, callback=callback, bouncetime=50)

    def remove_callback(self):
        """ Test """
        GPIO.remove_event_detect(self.gpio_no)

    def add_switches(self):
        """ Test """
        self.btn_state = GPIO.input(self.gpio_no)

    def check_switch(self):
        """ Test """
        self.btn_state = GPIO.input(self.gpio_no)

        # if changes the state of button return something.
        # If stay the state, will be returned nothing.
        if self.btn_state:
            if self.sec_state == 0:
                self.sec_state = 1
                return True
        else:
            if self.sec_state == 1:
                self.sec_state = 0
                return False

        if self.sec_state is None:
            if self.btn_state:
                self.sec_state = 1
                return True
            else:
                self.sec_state = 0
                return False
        return None

    def check_switch_once(self):
        """ Test """
        self.btn_state = GPIO.input(self.gpio_no)

        if self.btn_state:
            return True
        else:
            return False
