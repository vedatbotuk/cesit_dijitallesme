#!/usr/bin/python3
from RPi import GPIO

class Gpios(object):
    """Library for quad 7-segment LED modules based on the TM1637 LED driver."""
    def __init__(self, btn, dio, brightness=7):
        self.btn = btn
        self.state = self.state

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # GPIO.setwarnings(False)


        if not 0 <= brightness <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = brightness

        GPIO.setup(clk, GPIO.OUT)
        GPIO.setup(dio, GPIO.OUT)
        GPIO.output(clk, 0)
        GPIO.output(dio, 0)

        sleep(TM1637_DELAY)

        self._write_data_cmd()
        self._write_dsp_ctrl()