# # Erforderliche Bibliotheken importieren
# import RPi.GPIO as GPIO
# import time
#
# # Konvention für Pinnummerierung festlegen (BCM bzw. Board)
# GPIO.setmode(GPIO.BCM)
# # Pin mit seiner Nummer und als Ausgang definieren
# GPIO.setup(21, GPIO.OUT)
#
# for x in range(0, 5):
#     # Pin auf 3,3 V schalten
#     GPIO.output(21, GPIO.HIGH)
#     time.sleep(2)
#     # Pin auf 0 V schalten
#     GPIO.output(21, GPIO.LOW)
#     time.sleep(2)
#
# GPIO.cleanup()

import RPi.GPIO as GPIO
from time import sleep
from datetime import date
import json

data_js = {}

btn_counter = 17
btn_reset = 27
counter_nr = 0

btn_start_stop = 22
start_stop_state = 0


# led = 21


def setup():
    global data_js

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn_counter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_start_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(led, GPIO.OUT)

    data = {
        "Devices": {
            "Makine Pilot": {
                "Makine Durumu": "Çalışıyor",
                "Counter": "0",
                "Son Reset Tarihi": "20.03.2021 13:12"
            },
            "Makine 1": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "20.03.2021 13:12"
            },
            "Makine 2": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "20.03.2021 13:12"
            },
            "Makine 3": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "20.03.2021 13:12"
            },
            "Makine 4": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "20.03.2021 13:12"
            },
            "Makine  5": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "20.03.2021 13:12"
            }
        }
    }
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)

    def write_json(what, state):
        pass

    def loop():
        global counter_nr
        global data_js
        global start_stop_state

        while True:

            with open('data.json', 'w') as json_file:
                json.dump(data, json_file)

            for x in range(0, 300):
                button_state = GPIO.input(btn_counter)
                if button_state:
                    counter_nr = counter_nr + 1
                    print('Counter Pressed = ' + str(counter_nr))
                    sleep(1)
                    write_json('counter', counter_nr)

                button_state = GPIO.input(btn_reset)
                if button_state:
                    counter_nr = 0
                    today = date.today()
                    d2 = today.strftime("%B %d, %Y")
                    print('Reset' + ":" + d2)
                    sleep(1)

                    write_json('Reset', d2)

                button_state = GPIO.input(btn_start_stop)
                if button_state:
                    if start_stop_state == 0:
                        print('Start')
                        write_json('start', 1)
                        start_stop_state = 1
                else:
                    if start_stop_state == 1:
                        print('Stop')
                        write_json('stop', 0)
                        start_stop_state = 0

                sleep(0.2)

    # def loop():
    #     for x in range(0, 100):
    #         button_state = GPIO.input(button)
    #         if not button_state:
    #             GPIO.output(led, True)
    #             print('Button Pressed...')
    #             while not GPIO.input(button):
    #                 time.sleep(0.5)
    #         else:
    #             GPIO.output(led, False)
    #             GPIO.setup(led, GPIO.OUT)
    #
    #         time.sleep(0.5)

    # def endprogram():
    #     GPIO.output(led, False)

    if __name__ == '__main__':

        setup()

        try:
            # loop()
            GPIO.cleanup()

        except KeyboardInterrupt:
            print('keyboard interrupt detected')
            # endprogram()
            GPIO.cleanup()
