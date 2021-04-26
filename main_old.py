#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import json

data = {}

btn_counter = 17
btn_reset = 27
counter_nr = 0

btn_start_stop = 22
start_stop_state = 0

btn_bobin = 5
bobin_state = 0

btn_cozgu = 6
cozgu_state = 0

btn_ariza = 13
ariza_state = 0

btn_ayar = 19
ayar_state = 0


def setup():
    global data

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn_counter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_start_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_bobin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_cozgu, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_ariza, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_ayar, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    data = {
        "Devices": {
            "Makine Pilot": {
                "Makine Durumu": "Çalışıyor",
                "Counter": "0",
                "Son Reset Tarihi": "-"
            },
            "Makine 1": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "-"
            },
            "Makine 2": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "-"
            },
            "Makine 3": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "-"
            },
            "Makine 4": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "-"
            },
            "Makine  5": {
                "Makine Durumu": "Duruyor",
                "Counter": "0",
                "Son Reset Tarihi": "-"
            }
        }
    }
    with open('/var/www/html/data.json', 'w') as json_file:
        json.dump(data, json_file)


def change_json(what, state):
    if what == 'start':
        data['Devices']['Makine Pilot']['Makine Durumu'] = 'Çalışıyor'

    elif what == 'stop':
        data['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor'

    elif what == 'counter':
        data['Devices']['Makine Pilot']['Counter'] = state

    elif what == 'date':
        data['Devices']['Makine Pilot']['Son Reset Tarihi'] = state

    elif what == 'bobin':
        data['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor - Bobin değişimi'

    elif what == 'cozgu':
        data['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor - Çözgü'

    elif what == 'ariza':
        data['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor - Arıza'

    elif what == 'ayar':
        data['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor - Ayar'

    with open('/var/www/html/data.json', 'w') as json_file:
        json.dump(data, json_file)


def loop():
    global counter_nr
    global data
    global start_stop_state
    global bobin_state
    global cozgu_state
    global ariza_state
    global ayar_state

    while True:
        for x in range(0, 300):
            button_state = GPIO.input(btn_counter)
            if button_state:
                if start_stop_state == 1:
                    counter_nr = counter_nr + 1
                    # print('Counter Pressed = ' + str(counter_nr))
                    sleep(1)
                    change_json('counter', counter_nr)

            button_state = GPIO.input(btn_reset)
            if button_state:
                counter_nr = 0
                datetimeobj = datetime.now()
                d2 = datetimeobj.strftime("%d-%b-%Y (%H:%M:%S)")
                # print('Reset' + ":" + d2)
                change_json('date', d2)
                sleep(1)

                change_json('Reset', d2)
                change_json('counter', 0)

            # start stop und nebenarbeiten an der maschine
            button_state = GPIO.input(btn_start_stop)
            if button_state:
                # switch on
                if start_stop_state == 0:
                    # print('Start')
                    change_json('start', None)
                    start_stop_state = 1
            else:
                # switch off
                if start_stop_state == 1:
                    # print('Stop')
                    change_json('stop', None)
                    start_stop_state = 0

                # ab hier testet alle nebenarbeiten an der maschine
                button_state = GPIO.input(btn_bobin)
                if button_state:
                    if bobin_state == 0:
                        # print('Bobin')
                        change_json('bobin', None)
                        bobin_state = 1
                else:
                    if bobin_state == 1:
                        change_json('stop', None)
                        bobin_state = 0

                button_state = GPIO.input(btn_cozgu)
                if button_state:
                    if cozgu_state == 0:
                        # print('Cozgu')
                        change_json('cozgu', None)
                        cozgu_state = 1
                else:
                    if cozgu_state == 1:
                        change_json('stop', None)
                        cozgu_state = 0

                button_state = GPIO.input(btn_ariza)
                if button_state:
                    if ariza_state == 0:
                        # print('Ariza')
                        change_json('ariza', None)
                        ariza_state = 1
                else:
                    if ariza_state == 1:
                        change_json('stop', None)
                        ariza_state = 0

                button_state = GPIO.input(btn_ayar)
                if button_state:
                    if ayar_state == 0:
                        # print('Ayar')
                        change_json('ayar', None)
                        ayar_state = 1
                else:
                    if ayar_state == 1:
                        change_json('stop', None)
                        ayar_state = 0

            sleep(0.2)


if __name__ == '__main__':

    setup()

    try:
        loop()
        GPIO.cleanup()

    except KeyboardInterrupt:
        print('keyboard interrupt detected')
        # endprogram()
        GPIO.cleanup()
