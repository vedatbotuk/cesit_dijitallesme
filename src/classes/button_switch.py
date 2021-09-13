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

    # def __init__(self, gpio_funk, gpio_no, json_value_if, json_value_else):
    # gpio_no = None
    GPIO.setmode(GPIO.BCM)

    def __init__(self, gpio_no, callback=None):
        """ Description """

        config_json = get_setup()
        logging = LogInfo(config_json['main']['log'],
                          config_json['main']['log_level'],
                          config_json['main']['log_path'])

        # self.gpio_funk = gpio_funk
        self.gpio_no = gpio_no
        self.callback = callback

        if self.callback:
            GPIO.setup(self.gpio_no, GPIO.IN)
            # kwargs = {}
            # kwargs['callback'] = callback
            GPIO.add_event_detect(self.gpio_no, GPIO.RISING, callback=self.callback, bouncetime=800)
            logging.log_info('Switch configured at GPIO' + str(self.gpio_no))
            # GPIO.add_event_detect(gpio_no, GPIO.RISING, **kwargs)
        else:
            self.sec_state = 0

            GPIO.setup(self.gpio_no, GPIO.IN)
            self.btn_state = GPIO.input(self.gpio_no)

            logging.log_info('Switch configured at GPIO' + str(self.gpio_no))

    # GPIO.setwarnings(False)

    # @classmethod
    # def add_event_detect(cls, func):
    #     GPIO.add_event_detect(cls.gpio_no, GPIO.RISING, func, bouncetime=200)

    def check_switch(self):
        """ Test """

        self.btn_state = GPIO.input(self.gpio_no)

        # self.btn_state = GPIO.input(self.gpio_no)
        # if changes the state of button return something.
        # If stay the state, will be returned nothing.
        if self.btn_state:
            # machine on, hat Strom
            if self.sec_state == 0:
                # print('kapali')
                # write_lcd('kapali', None)
                # change_json('kapali', None)
                self.sec_state = 1
                return True
        else:
            # machine off
            if self.sec_state == 1:
                # print('Acik')
                # write_lcd('stop', None)
                # change_json('stop', None)
                self.sec_state = 0
                return False
