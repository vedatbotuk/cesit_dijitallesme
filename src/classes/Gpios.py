#!/usr/bin/python3
''' Description '''

from RPi import GPIO
from RPLCD.i2c import CharLCD

class ButtonSwitch(object):
    """Library for quad 7-segment LED modules based on the TM1637 LED driver."""

    # def __init__(self, gpio_funk, gpio_no, json_value_if, json_value_else):
    def __init__(self, gpio_no, callback = None):
        
        GPIO.setmode(GPIO.BCM)
        
        # self.gpio_funk = gpio_funk
        self.gpio_no = gpio_no
        self.callback = callback
        
        if callback:
            GPIO.setup(self.gpio_no, GPIO.IN)
            kwargs = {}
            kwargs['callback']=callback
            # GPIO.add_event_detect(self.gpio_no, GPIO.RISING, **kwargs, bouncetime=200)
            GPIO.add_event_detect(gpio_no, GPIO.RISING, **kwargs)
        else:
            self.sec_state = 0
    
            GPIO.setup(self.gpio_no, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.btn_state = GPIO.input(self.gpio_no)
            

    # GPIO.setwarnings(False)
    def check(self):
        ''' Test '''
        
        self.btn_state = GPIO.input(self.gpio_no)
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

class LcdModule(object):
    ''' Description '''

    def __init__(self, modell = 'PCF8574', address = 0x27):
        self.modell = modell
        self.address = address

        self.lcd = CharLCD(modell, address)
        

    def write_row1(self):
        ''' Description '''
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(self)

    def write_row2(self):
        ''' Description '''
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(self)







