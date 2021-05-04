# !/usr/bin/python3
''' Description '''

import json
import os
from time import sleep

from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import classes as classes


time_obj = classes.Time()
bobin_btn = classes.ButtonSwitch(5)

lcd = CharLCD('PCF8574', 0x27)

system_time = ''

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

# btn_bobin = 5
# bobin_state = 0

btn_cozgu = 6
cozgu_state = 0

btn_ariza = 13
ariza_state = 0

btn_ayar = 19
ayar_state = 0

path_json = '/var/www/html/data.json'
path_json_default = 'default_data.json'


def setup():
    '''Takes in a number n, returns the square of n'''
    global data_js
    global counter_nr

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(btn_kapali, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_counter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_start_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(btn_bobin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_cozgu, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_ariza, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_ayar, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # if not exists create file
    if os.path.isfile(path_json):
        data_js = json.load(open(path_json, 'r'))
        counter_nr = int(data_js['Devices']['Makine Pilot']['Counter'])

    else:
        with open(path_json_default, 'r') as json_file:
            json.dump(data_js, json_file)


def change_json(what, state):
    '''change_json'''
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

    with open(path_json, 'w') as json_file:
        json.dump(data_js, json_file)


def write_lcd(what, show):
    ''' Description '''
    global system_time

    if what == 'kapali':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(system_time + '    ' + u'kapali')

    elif what == 'start':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(system_time + ' ' + u'calisiyor')

    elif what == 'stop':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(system_time + '   ' + u'duruyor')

    elif what == 'bobin':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(system_time + '     ' + u'bobin')

    elif what == 'cozgu':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(system_time + '     ' + u'cozgu')

    elif what == 'ariza':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(system_time + '     ' + u'ariza')

    elif what == 'ayar':
        lcd.cursor_pos = (0, 0)
        lcd.write_string(system_time + '      ' + u'ayar')

    elif what == 'reset':
        lcd.cursor_pos = (1, 0)
        lcd.write_string(u'Counter= ' + '0      ')

    elif what == 'counter':
        lcd.cursor_pos = (1, 0)
        lcd.write_string(u'Counter= ' + str(show))


def gpio_check():
    ''' Description '''
    global counter_nr
    global start_stop_state
    global bobin_state
    global cozgu_state
    global ariza_state
    global ayar_state
    global kapali_state
    global reset_state
    global counter_state


    # AC/KAPA SWITCH ###########################
    button_state_kapali = GPIO.input(btn_kapali)
    if button_state_kapali:
        # machine off, kapali
        if kapali_state == 0:
            # print('kapali')
            write_lcd('kapali', None)
            change_json('kapali', None)
            kapali_state = 1

    else:
        # machine on, acik
        if kapali_state == 1:
            # print('Acik')
            write_lcd('stop', None)
            change_json('stop', None)
            kapali_state = 0

        # COUNTER BUTTON #############################
        button_state_counter = GPIO.input(btn_counter)
        if button_state_counter:
            if counter_state == 0:
                counter_nr = counter_nr + 1
                # print('Counter Pressed = ' + str(counter_nr))
                write_lcd('counter', counter_nr)
                change_json('counter', counter_nr)
                counter_state = 1
        else:
            # sicherung, wenn die Taste gedruck bleibt
            if counter_state == 1:
                counter_state = 0
        # COUNTER BUTTON ##

        # START/STOP SWITCH ################################
        # start stop und nebenarbeiten an der maschine
        # wenn start switch on, zeigt nur start bzw. calisiyor
        button_state_start_stop = GPIO.input(btn_start_stop)
        if button_state_start_stop:
            # switch on
            write_lcd('start', None)
            if start_stop_state == 0:
                # print('Start')
                change_json('start', None)
                start_stop_state = 1
        # maschiene gestopt
        # zusatzlich kann signalisiert werden, warum die maschine gestopt
        else:
            # switch off
            if start_stop_state == 1:
                # print('Stop')
                write_lcd('stop', None)
                change_json('stop', None)
                start_stop_state = 0

            # RESET BUTTON ###########################
            button_state_reset = GPIO.input(btn_reset)
            if button_state_reset:
                if reset_state == 0:
                    counter_nr = 0
                    # print('Reset' + ":" + co)
                    write_lcd('reset', counter_nr)
                    change_json('reset', time_obj.get_date_time())
                    change_json('counter', 0)
                    reset_state = 1
            else:
                # sicherung, wenn die Taste gedruck bleibt
                if reset_state == 1:
                    reset_state = 0
            # RESET BUTTON ##

            # BOBIN SWITCH ###########################
            # ab hier testet alle nebenarbeiten an der maschine
            if bobin_btn.check() is True:
                write_lcd('bobin', None)
                change_json('bobin', None)
            else:
                write_lcd('stop', None)
                change_json('stop', None)

            # button_state_bobin = GPIO.input(btn_bobin)
            # if button_state_bobin:
            #     if bobin_state == 0:
            #         # print('Bobin')
            #         write_lcd('bobin', None)
            #         change_json('bobin', None)
            #         bobin_state = 1
            # else:
            #     if bobin_state == 1:
            #         write_lcd('stop', None)
            #         change_json('stop', None)
            #         bobin_state = 0
            # BOBIN SWITCH ##

            # COZGU SWITCH ###########################
            button_state_cozgu = GPIO.input(btn_cozgu)
            if button_state_cozgu:
                if cozgu_state == 0:
                    # print('Cozgu')
                    write_lcd('cozgu', None)
                    change_json('cozgu', None)
                    cozgu_state = 1
            else:
                if cozgu_state == 1:
                    write_lcd('stop', None)
                    change_json('stop', None)
                    cozgu_state = 0
            # COZGU SWITCH ##

            # ARIZA SWITCH ###########################
            button_state_ariza = GPIO.input(btn_ariza)
            if button_state_ariza:
                if ariza_state == 0:
                    # print('Ariza')
                    write_lcd('ariza', None)
                    change_json('ariza', None)
                    ariza_state = 1
            else:
                if ariza_state == 1:
                    write_lcd('stop', None)
                    change_json('stop', None)
                    ariza_state = 0
            # ARIZA SWITCH ##

            # AYAR SWITCH ###########################
            button_state_ayar = GPIO.input(btn_ayar)
            if button_state_ayar:
                if ayar_state == 0:
                    # print('Ayar')
                    write_lcd('ayar', None)
                    change_json('ayar', None)
                    ayar_state = 1
            else:
                if ayar_state == 1:
                    write_lcd('stop', None)
                    change_json('stop', None)
                    ayar_state = 0
            # AYAR SWITCH ##
        # START/STOP SWITCH ##
    # AC/KAPA SWITCH ##


def loop():
    ''' Description '''
    global system_time

    while True:
        gpio_check()
        system_time = time_obj.sync()
        sleep(0.2)


def check_sytem_up():
    ''' Description '''
    global counter_nr
    global start_stop_state
    global bobin_state
    global cozgu_state
    global ariza_state
    global ayar_state
    global kapali_state
    global reset_state
    global counter_state

    write_lcd('counter', counter_nr)

    button_state_kapali = GPIO.input(btn_kapali)
    if button_state_kapali:

        write_lcd('kapali', None)
        change_json('kapali', None)
        kapali_state = 0

    else:
        kapali_state = 1

        button_state_start_stop = GPIO.input(btn_start_stop)
        if button_state_start_stop:
            # switch on
            write_lcd('start', None)
            # print('Start')
            change_json('start', None)
            start_stop_state = 1

        else:
            write_lcd('stop', None)
            change_json('stop', None)
            start_stop_state = 0


            if bobin_btn.check() is True:
                write_lcd('bobin', None)
                change_json('bobin', None)
            else:
                write_lcd('stop', None)
                change_json('stop', None)
            # button_state_bobin = GPIO.input(btn_bobin)
            # if button_state_bobin:
            #     write_lcd('bobin', None)
            #     change_json('bobin', None)
            #     bobin_state = 1
            # else:
            #     write_lcd('stop', None)
            #     change_json('stop', None)
            #     bobin_state = 0

            button_state_cozgu = GPIO.input(btn_cozgu)
            if button_state_cozgu:
                write_lcd('cozgu', None)
                change_json('cozgu', None)
                cozgu_state = 1
            else:
                write_lcd('stop', None)
                change_json('stop', None)
                cozgu_state = 0

            button_state_ariza = GPIO.input(btn_ariza)
            if button_state_ariza:
                write_lcd('ariza', None)
                change_json('ariza', None)
                ariza_state = 1
            else:
                write_lcd('stop', None)
                change_json('stop', None)
                ariza_state = 0

            button_state_ayar = GPIO.input(btn_ayar)
            if button_state_ayar:
                write_lcd('ayar', None)
                change_json('ayar', None)
                ayar_state = 1
            else:
                write_lcd('stop', None)
                change_json('stop', None)
                ayar_state = 0


if __name__ == '__main__':
    setup()

    try:
        check_sytem_up()
        loop()
        GPIO.cleanup()

    except KeyboardInterrupt:
        print('keyboard interrupt detected')
        # endprogram()
        GPIO.cleanup()

