#!/usr/bin/python3
""" Description """

from RPi import GPIO
from RPLCD.i2c import CharLCD


def gpio_cleanup():
    GPIO.cleanup()


class ButtonSwitch:
    """Library for quad 7-segment LED modules based on the TM1637 LED driver."""

    # def __init__(self, gpio_funk, gpio_no, json_value_if, json_value_else):
    gpio_no = None

    def __init__(self, gpio_no, callback=None):

        GPIO.setmode(GPIO.BCM)

        # self.gpio_funk = gpio_funk
        self.gpio_no = gpio_no
        self.callback = callback

        if callback:
            GPIO.setup(self.gpio_no, GPIO.IN)
            # kwargs = {}
            # kwargs['callback'] = callback
            GPIO.add_event_detect(self.gpio_no, GPIO.RISING, callback, bouncetime=1000)
            # GPIO.add_event_detect(gpio_no, GPIO.RISING, **kwargs)
        else:
            self.sec_state = 0

            GPIO.setup(self.gpio_no, GPIO.IN)
            self.btn_state = GPIO.input(self.gpio_no)

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


class LcdModule:
    """ Description """

    # lcd = None

    lcd = CharLCD('PCF8574', address=0x27)

    def __init__(self, model='PCF8574', address=0x27):
        self.text = ''
        self.model = model
        self.address = address

        self.lcd = CharLCD(model, address)

    @classmethod
    def write_row1(cls, text):
        """ Description """
        cls.lcd.cursor_pos = (0, 0)
        cls.lcd.write_string(text)

    @classmethod
    def write_row2(cls, text):
        """ Description """
        cls.lcd.cursor_pos = (1, 0)
        cls.lcd.write_string(text)
