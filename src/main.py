#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

# Imports
from time import sleep
import classes

# Setup
CONFIG_JSON = classes.get_setup()

LOGGING = classes.LogInfo(CONFIG_JSON['main']['log'],
                          CONFIG_JSON['main']['log_level'],
                          CONFIG_JSON['main']['log_path'])

LOGGING.log_info('--- System starting ---')

SYSTEM_TIME = ''
MACHINE_START_STOP = 0
system_on = 0
stop_options_array = []

JSON_FUNCS = classes.JsonFuncs()
COUNTER_NR = JSON_FUNCS.get_counter()

LCD = classes.LcdModule()
BTN_KAPALI = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_kapali'])
BTN_START_STOP = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_start_stop'])
BTN_COZGU = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_cozgu'])
BTN_ARIZA = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_ariza'])
BTN_AYAR = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_ayar'])
BTN_BOBIN = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_bobin'])

BTN_COUNTER = classes.ButtonSwitch(CONFIG_JSON['buttons']['btn_counter'])


def gpio_check():
    """ Description """
    global MACHINE_START_STOP,\
        COUNTER_NR,\
        BTN_START_STOP,\
        BTN_BOBIN,\
        BTN_COZGU,\
        BTN_ARIZA,\
        BTN_AYAR,\
        BTN_KAPALI,\
        system_on, \
        stop_options_array

    options_changed = 0

    # AC/KAPA SWITCH
    # ###########################
    btn_kapali_checked = BTN_KAPALI.check_switch()
    if btn_kapali_checked is False:
        stop_options_array.append('kapali')
        system_on = 0
        options_changed = 1
        LOGGING.log_info('Device off')
    elif btn_kapali_checked is True:
        if 'kapali' in stop_options_array:
            stop_options_array.remove('kapali')
        stop_options_array.append('stop')
        system_on = 1
        options_changed = 1
        LOGGING.log_info('Device stopped')
    # AC/KAPA SWITCH ------------
    # ---------------------------

    if system_on == 1:
        # START/STOP SWITCH ##############
        # ################################
        # start stop und nebenarbeiten an der maschine
        # wenn start switch on, zeigt nur start bzw. calisiyor
        btn_start_stop_checked = BTN_START_STOP.check_switch()
        if btn_start_stop_checked is False:
            if 'stop' in stop_options_array:
                stop_options_array.remove('stop')
            stop_options_array.append('start')
            MACHINE_START_STOP = 1
            options_changed = 1
            LOGGING.log_info('Device started')
        # maschiene gestopt
        # zusatzlich kann signalisiert werden, warum die maschine gestopt
        elif btn_start_stop_checked is True:
            if 'start' in stop_options_array:
                stop_options_array.remove('start')
            stop_options_array.append('stop')
            MACHINE_START_STOP = 0
            options_changed = 1
            LOGGING.log_info('Device stopped')
        # START/STOP SWITCH --------
        # ---------------------------

    if MACHINE_START_STOP == 0 and system_on == 1:
        # BOBIN SWITCH ##############
        # ###########################
        # ab hier testet alle nebenarbeiten an der maschine
        btn_bobin_checked = BTN_BOBIN.check_switch()
        if btn_bobin_checked is False:
            stop_options_array.append('bobin')
            options_changed = 1
            LOGGING.log_info('Device at bobin-status')
        elif btn_bobin_checked is True:
            if 'bobin' in stop_options_array:
                stop_options_array.remove('bobin')
            options_changed = 1
            LOGGING.log_info('Device exited bobin-status')
        # BOBIN SWITCH --------------
        # ---------------------------

        # COZGU SWITCH ##############
        # ###########################
        btn_cozgu_checked = BTN_COZGU.check_switch()
        if btn_cozgu_checked is False:
            stop_options_array.append('cozgu')
            options_changed = 1
            LOGGING.log_info('Device exited cozgu-status')
        elif btn_cozgu_checked is True:
            if 'cozgu' in stop_options_array:
                stop_options_array.remove('cozgu')
            options_changed = 1
            LOGGING.log_info('Device exited cozgu-status')
        # COZGU SWITCH --------------
        # ---------------------------

        # ARIZA SWITCH ##############
        # ###########################
        btn_ariza_checked = BTN_ARIZA.check_switch()
        if btn_ariza_checked is False:
            stop_options_array.append('ariza')
            options_changed = 1
            LOGGING.log_info('Device exited ariza-status')
        elif btn_ariza_checked is True:
            if 'ariza' in stop_options_array:
                stop_options_array.remove('ariza')
            options_changed = 1
            LOGGING.log_info('Device exited azriza-status')
        # ARIZA SWITCH --------------
        # ---------------------------

        # AYAR SWITCH ###############
        # ###########################
        btn_ayar_checked = BTN_AYAR.check_switch()
        if btn_ayar_checked is False:
            stop_options_array.append('ayar')
            options_changed = 1
            LOGGING.log_info('Device exited ayar-status')
        elif btn_ayar_checked is True:
            if 'ayar' in stop_options_array:
                stop_options_array.remove('ayar')
            options_changed = 1
            LOGGING.log_info('Device exited ayar-status')
        # AYAR SWITCH ---------------
        # ---------------------------

    LCD.refresh_lcd(stop_options_array[len(stop_options_array) - 1], COUNTER_NR)

    # if options_changed == 1 and stop_options_array:
    #     # last entry in array
    #     LCD.write_lcd(stop_options_array[len(stop_options_array) - 1], None)
    #     JSON_FUNCS.change_json(what=stop_options_array[len(stop_options_array) - 1])


def loop():
    """ Description """
    global SYSTEM_TIME

    LOGGING.log_info('gpio_check loop begins.')
    while True:
        gpio_check()
        # SYSTEM_TIME = LCD.sync_time()
        sleep(0.2)


def write_lcd_json_counter(channel):
    """ Description """
    global COUNTER_NR, MACHINE_START_STOP, BTN_COUNTER

    if MACHINE_START_STOP == 1:
        btn_counter_checked = BTN_COUNTER.check_switch()
        if btn_counter_checked is False:
            sleep(0.1)
            COUNTER_NR = COUNTER_NR + 1
            # LCD.write_lcd('counter', COUNTER_NR)
            # JSON_FUNCS.change_json(what='counter', state=COUNTER_NR)
            LOGGING.log_info(channel)


def write_lcd_json_btn_reset(channel):
    """ Description """
    global COUNTER_NR, MACHINE_START_STOP

    if MACHINE_START_STOP == 0:
        COUNTER_NR = 0
        # LCD.write_lcd('reset', COUNTER_NR)
        # JSON_FUNCS.change_json(what='reset')
        # JSON_FUNCS.change_json(what='counter', state=0)
        LOGGING.log_info('Counter rested.')
        LOGGING.log_info(channel)


classes.ButtonSwitch(CONFIG_JSON['buttons']['btn_counter'], callback=write_lcd_json_counter)
classes.ButtonSwitch(CONFIG_JSON['buttons']['btn_reset'], callback=write_lcd_json_btn_reset)

if __name__ == '__main__':
    LOGGING.log_info('System loaded.')
    try:
        loop()
        classes.gpio_cleanup()

    except KeyboardInterrupt:
        print('keyboard interrupt detected')
        LOGGING.log_info('System stopped.')
        classes.gpio_cleanup()
        LCD.lcd_close()
    # end of program
