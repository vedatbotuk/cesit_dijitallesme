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
        self.sec_state = 0
        self.btn_state = None

        GPIO.setup(self.gpio_no, GPIO.IN)

    def add_callback(self, callback):
        """ Test """
        GPIO.add_event_detect(self.gpio_no, GPIO.RISING, callback=callback)

    def remove_callback(self):
        """ Test """
        GPIO.remove_event_detect(self.gpio_no)
        self.logging.log_info('Switch configured at GPIO' + str(self.gpio_no))

    def wait_for(self):
        """ Test """
        callback = GPIO.wait_for_edge(self.gpio_no, GPIO.FALLING, timeout=2000)
        return callback

    def add_switches(self):
        """ Test """
        self.sec_state = 0

        self.btn_state = GPIO.input(self.gpio_no)
        self.logging.log_info('Switch configured at GPIO' + str(self.gpio_no))

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
