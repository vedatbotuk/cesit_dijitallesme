# cesit_dijitallesme

# Install

## Raspbian OS

## Python

## VPN

# Requirements
- ```pip3 install pymongo RPLCD smbus2 ```
- ```pip3 install "paho-mqtt<2.0.0"```

# Hardware

# Remarks
- An external pull-up sensor is being used.
If an internal pull-up must be used, the entry `pull_up_down=GPIO.PUD_OFF` in `button_switch.py` within the line `GPIO.setup(self.gpio_no, GPIO.IN, pull_up_down=GPIO.PUD_OFF)` needs to be removed.
- A hex inverter is used before the GPIO input, so the signals are inverted.
- Currently, a 1 microfarad capacitor is installed for debouncing, which is very large. Either remove it or replace it with a 0.1 microfarad capacitor.
