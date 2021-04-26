#!/usr/bin/python3
import os
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import json
from RPLCD.i2c import CharLCD







lcd = CharLCD('PCF8574', 0x27)

system_time = None
data_js = {}

btn_kapali = 4
kapali_state = 0

btn_counter = 17
counter_state = 0

btn_reset = 27
reset_state = 0
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
    global data_js

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn_kapali, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_counter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_start_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_bobin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_cozgu, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_ariza, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_ayar, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # if not exists create file
    if os.path.isfile('/var/www/html/data.json'):
        data_js = json.load(open('/var/www/html/data.json', 'r'))
    else:
        with open('default_data.json', 'w') as json_file:
            json.dump(data_js, json_file)


def change_json(what, state):
    if what == 'kapali':
        data_js['Devices']['Makine Pilot']['Makine Durumu'] = 'Kapalı'

    elif what == 'start':
        data_js['Devices']['Makine Pilot']['Makine Durumu'] = 'Çalışıyor'

    elif what == 'stop':
        data_js['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor'

    elif what == 'counter':
        data_js['Devices']['Makine Pilot']['Counter'] = state

    elif what == 'reset':
        data_js['Devices']['Makine Pilot']['Son Reset Tarihi'] = state

    elif what == 'bobin':
        data_js['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor - Bobin değişimi'

    elif what == 'cozgu':
        data_js['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor - Çözgü'

    elif what == 'ariza':
        data_js['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor - Arıza'

    elif what == 'ayar':
        data_js['Devices']['Makine Pilot']['Makine Durumu'] = 'Duruyor - Ayar'

    with open('/var/www/html/data.json', 'w') as json_file:
        json.dump(data_js, json_file)


def write_lcd(what, show):
    date_wl = get_date_time('basic')

    if what == 'kapali':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(date_wl + '    ' + u'kapali')

    elif what == 'start':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(date_wl + ' ' + u'calisiyor')

    elif what == 'stop':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(date_wl + '   ' + u'duruyor')

    elif what == 'bobin':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(date_wl + '     ' + u'bobin')

    elif what == 'cozgu':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(date_wl + '     ' + u'cozgu')

    elif what == 'ariza':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(date_wl + '     ' + u'ariza')

    elif what == 'ayar':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(date_wl + '      ' + u'ayar')

    elif what == 'counter':
        lcd.cursor_pos = (1, 0)
        lcd.write_string(u'Counter= ' + show)


def get_date_time(which):
    date_time_obj = datetime.now()

    if which == 'long':
        return date_time_obj.strftime("%d-%b-%Y (%H:%M:%S)")


def sync_time():
    global system_time
    date_time_obj = datetime.now()

    if system_time != date_time_obj.strftime("%H:%M"):
        system_time = date_time_obj.strftime("%H:%M")


def check_btn(name_btn, name_state, name_json, name_nr_status):
    if name_btn == 1:
        if name_state == 0:
            if (type(name_nr_status)) == int:
                name_nr = name_nr_status + 1

            change_json(name_json, name_nr_status)
            name_state = 1
            print(name_json + '= ' + name_nr_status)


def gpio_check():
    global counter_nr
    global start_stop_state
    global bobin_state
    global cozgu_state
    global ariza_state
    global ayar_state
    global kapali_state
    global reset_state
    global counter_state

    button_state_counter = GPIO.input(btn_counter)
    if button_state_counter:
        if start_stop_state == 1:
            if counter_state == 0:
                counter_nr = counter_nr + 1
                # print('Counter Pressed = ' + str(counter_nr))
                change_json('counter', counter_nr)
                counter_state = 1
    else:
        # sicherung, wenn die Taste gedruck bleibt
        if counter_state == 1:
            counter_state = 0

    button_state_reset = GPIO.input(btn_reset)
    if button_state_reset:
        if reset_state == 0:
            counter_nr = 0
            # print('Reset' + ":" + d2)
            change_json('reset', get_date_time('long'))
            change_json('counter', 0)
            reset_state = 1
    else:
        # sicherung, wenn die Taste gedruck bleibt
        if reset_state == 1:
            reset_state = 0

    #
    # ##
    button_state_kapali = GPIO.input(btn_kapali)
    if button_state_kapali:
        # machine on, hat Strom
        if kapali_state == 0:
            # print('Acik')
            # change_json('start', None)
            start_stop_state = 1

        # start stop und nebenarbeiten an der maschine
        # wenn start switch on, zeigt nur start bzw. calisiyor
        button_state_start_stop = GPIO.input(btn_start_stop)
        if button_state_start_stop:
            # switch on
            if start_stop_state == 0:
                # print('Start')
                change_json('start', None)
                start_stop_state = 1

        # maschiene gestopt
        # zusatzlich kann signalisiert werden, warum die maschine gestopt
        else:
            #
            # switch off
            if start_stop_state == 1:
                # print('Stop')
                change_json('stop', None)
                start_stop_state = 0

            #
            # ###
            # ab hier testet alle nebenarbeiten an der maschine
            button_state_bobin = GPIO.input(btn_bobin)
            if button_state_bobin:
                if bobin_state == 0:
                    # print('Bobin')
                    change_json('bobin', None)
                    bobin_state = 1
            else:
                if bobin_state == 1:
                    change_json('stop', None)
                    bobin_state = 0

            button_state_cozgu = GPIO.input(btn_cozgu)
            if button_state_cozgu:
                if cozgu_state == 0:
                    # print('Cozgu')
                    change_json('cozgu', None)
                    cozgu_state = 1
            else:
                if cozgu_state == 1:
                    change_json('stop', None)
                    cozgu_state = 0

            button_state_ariza = GPIO.input(btn_ariza)
            if button_state_ariza:
                if ariza_state == 0:
                    # print('Ariza')
                    change_json('ariza', None)
                    ariza_state = 1
            else:
                if ariza_state == 1:
                    change_json('stop', None)
                    ariza_state = 0

            button_state_ayar = GPIO.input(btn_ayar)
            if button_state_ayar:
                if ayar_state == 0:
                    # print('Ayar')
                    change_json('ayar', None)
                    ayar_state = 1
            else:
                if ayar_state == 1:
                    change_json('stop', None)
                    ayar_state = 0
            # ###
            #
    else:
        # machine off
        if kapali_state == 1:
            # print('kapali')
            change_json('kapali', None)
            kapali_state = 0
    # ##
    #



def loop():
    global system_time

    while True:
        gpio_check()
        sync_time()
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
