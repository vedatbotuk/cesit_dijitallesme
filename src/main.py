#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

# #######
# Imports
from time import sleep
import classes


# #####
# Setup
CONFIG_JSON = classes.get_setup()

LOGGING = classes.LogInfo(CONFIG_JSON['main']['log'],
                          CONFIG_JSON['main']['log_level'],
                          CONFIG_JSON['main']['log_path'])

LOGGING.log_info('--- System starting ---')

SYSTEM_TIME = ''
MACHINE_START_STOP = 0
SYSTEM_ON = 0
stop_options_array = []

JSON_FUNCS = classes.JsonFuncs()
COUNTER_NR = JSON_FUNCS.get_counter()

LCD = classes.LcdModule()
BTN_KAPALI = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_kapali'])
BTN_KAPALI.add_switches()
BTN_START_STOP = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_start_stop'])
BTN_START_STOP.add_switches()
BTN_COZGU = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_cozgu'])
BTN_COZGU.add_switches()
BTN_ARIZA = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_ariza'])
BTN_ARIZA.add_switches()
BTN_AYAR = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_ayar'])
BTN_AYAR.add_switches()
BTN_BOBIN = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_bobin'])
BTN_BOBIN.add_switches()

BTN_RESET = classes.ButtonSwitch(CONFIG_JSON['buttons']['btn_reset'])
BTN_COUNTER = classes.ButtonSwitch(CONFIG_JSON['buttons']['btn_counter'])
# end of setup
# ############


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
        SYSTEM_ON, \
        stop_options_array

    options_changed = 0

    # AC/KAPA SWITCH
    # ###########################
    btn_kapali_checked = BTN_KAPALI.check_switch()
    if btn_kapali_checked is True:
        BTN_RESET.add_callback(callback=write_lcd_json_btn_reset)
        stop_options_array.append('kapali')
        SYSTEM_ON = 0
        options_changed = 1
        LOGGING.log_info('Device off')
    elif btn_kapali_checked is False:
        BTN_RESET.remove_callback()
        if 'kapali' in stop_options_array:
            stop_options_array.remove('kapali')
        stop_options_array.append('stop')
        SYSTEM_ON = 1
        options_changed = 1
        LOGGING.log_info('Device stopped')
    # AC/KAPA SWITCH ------------
    # ---------------------------

    if SYSTEM_ON == 1:
        # START/STOP SWITCH ##############
        # ################################
        # start stop und nebenarbeiten an der maschine
        # wenn start switch on, zeigt nur start bzw. calisiyor
        btn_start_stop_checked = BTN_START_STOP.check_switch()
        if btn_start_stop_checked is True:
            BTN_COUNTER.add_callback(callback=write_lcd_json_counter)
            if 'stop' in stop_options_array:
                stop_options_array.remove('stop')
            stop_options_array.append('start')
            MACHINE_START_STOP = 1
            options_changed = 1
            LOGGING.log_info('Device started')
        # maschiene gestopt
        # zusatzlich kann signalisiert werden, warum die maschine gestopt
        elif btn_start_stop_checked is False:
            BTN_COUNTER.remove_callback()
            if 'start' in stop_options_array:
                stop_options_array.remove('start')
            stop_options_array.append('stop')
            MACHINE_START_STOP = 0
            options_changed = 1
            LOGGING.log_info('Device stopped')
        # START/STOP SWITCH --------
        # ---------------------------

    if MACHINE_START_STOP == 0 and SYSTEM_ON == 1:
        # BOBIN SWITCH ##############
        # ###########################
        # ab hier testet alle nebenarbeiten an der maschine
        btn_bobin_checked = BTN_BOBIN.check_switch()
        if btn_bobin_checked is True:
            if 'bobin' in stop_options_array:
                stop_options_array.remove('bobin')
            options_changed = 1
            LOGGING.log_info('Device exited bobin-status')
        elif btn_bobin_checked is False:
            stop_options_array.append('bobin')
            options_changed = 1
            LOGGING.log_info('Device at bobin-status')
        # BOBIN SWITCH --------------
        # ---------------------------

        # COZGU SWITCH ##############
        # ###########################
        btn_cozgu_checked = BTN_COZGU.check_switch()
        if btn_cozgu_checked is True:
            if 'cozgu' in stop_options_array:
                stop_options_array.remove('cozgu')
            options_changed = 1
            LOGGING.log_info('Device exited cozgu-status')
        elif btn_cozgu_checked is False:
            stop_options_array.append('cozgu')
            options_changed = 1
            LOGGING.log_info('Device exited cozgu-status')
        # COZGU SWITCH --------------
        # ---------------------------

        # ARIZA SWITCH ##############
        # ###########################
        btn_ariza_checked = BTN_ARIZA.check_switch()
        if btn_ariza_checked is True:
            if 'ariza' in stop_options_array:
                stop_options_array.remove('ariza')
            options_changed = 1
            LOGGING.log_info('Device exited azriza-status')
        elif btn_ariza_checked is False:
            stop_options_array.append('ariza')
            options_changed = 1
            LOGGING.log_info('Device exited ariza-status')
        # ARIZA SWITCH --------------
        # ---------------------------

        # AYAR SWITCH ###############
        # ###########################
        btn_ayar_checked = BTN_AYAR.check_switch()
        if btn_ayar_checked is True:
            if 'ayar' in stop_options_array:
                stop_options_array.remove('ayar')
            options_changed = 1
            LOGGING.log_info('Device exited ayar-status')
        elif btn_ayar_checked is False:
            stop_options_array.append('ayar')
            options_changed = 1
            LOGGING.log_info('Device exited ayar-status')
        # AYAR SWITCH ---------------
        # ---------------------------

    if stop_options_array:
        LCD.refresh_lcd(stop_options_array[len(stop_options_array) - 1], COUNTER_NR)

    if options_changed == 1 and stop_options_array:
        JSON_FUNCS.change_json(what=stop_options_array[len(stop_options_array) - 1])


def loop():
    """ Description """
    global SYSTEM_TIME

    LOGGING.log_info('gpio_check loop begins.')
    while True:
        gpio_check()
        sleep(0.1)


def write_lcd_json_counter(channel):
    """ Description """
    global COUNTER_NR, MACHINE_START_STOP

    if MACHINE_START_STOP == 1 and SYSTEM_ON == 1:
        btn_start_stop_checked = BTN_START_STOP.check_switch_once()
        if btn_start_stop_checked is True:
            COUNTER_NR = COUNTER_NR + 1
            JSON_FUNCS.change_json(what='counter', state=COUNTER_NR)
            LOGGING.log_info(channel)


def write_lcd_json_btn_reset(channel):
    """ Description """
    global COUNTER_NR, MACHINE_START_STOP, SYSTEM_ON

    # if MACHINE_START_STOP == 0 and SYSTEM_ON == 0:
    if MACHINE_START_STOP == 0:
        COUNTER_NR = 0
        JSON_FUNCS.change_json(what='reset')
        JSON_FUNCS.change_json(what='counter', state=0)
        LOGGING.log_info('Counter rested.')
        LOGGING.log_info(channel)


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
    # ##############
