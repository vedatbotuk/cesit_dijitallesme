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

MACHINE_START_STOP = 0
SYSTEM_ON = 0
OPTIONS_CHANGED = 1
STOP_OPTIONS_ARRAY = []

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

run_time = classes.StartStopWatch()
# end of setup
# ############


def check_kapali():
    """ Description """
    global SYSTEM_ON, OPTIONS_CHANGED
    # AC/KAPA SWITCH
    # ###########################
    btn_kapali_checked = BTN_KAPALI.check_switch()
    if btn_kapali_checked is True:
        STOP_OPTIONS_ARRAY.append('kapali')
        SYSTEM_ON = 0
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device off')
    elif btn_kapali_checked is False:
        if 'kapali' in STOP_OPTIONS_ARRAY:
            STOP_OPTIONS_ARRAY.remove('kapali')
        STOP_OPTIONS_ARRAY.append('stop')
        SYSTEM_ON = 1
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device on')
    # AC/KAPA SWITCH ------------
    # ---------------------------


def check_bobin():
    """ Description """
    global OPTIONS_CHANGED
    # BOBIN SWITCH ##############
    # ###########################
    # ab hier testet alle nebenarbeiten an der maschine
    btn_bobin_checked = BTN_BOBIN.check_switch()
    if btn_bobin_checked is True:
        if 'bobin' in STOP_OPTIONS_ARRAY:
            STOP_OPTIONS_ARRAY.remove('bobin')
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device exited bobin-status')
    elif btn_bobin_checked is False:
        STOP_OPTIONS_ARRAY.append('bobin')
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device at bobin-status')
    # BOBIN SWITCH --------------
    # ---------------------------


def check_cozgu():
    """ Description """
    global OPTIONS_CHANGED
    # COZGU SWITCH ##############
    # ###########################
    btn_cozgu_checked = BTN_COZGU.check_switch()
    if btn_cozgu_checked is True:
        if 'cozgu' in STOP_OPTIONS_ARRAY:
            STOP_OPTIONS_ARRAY.remove('cozgu')
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device exited cozgu-status')
    elif btn_cozgu_checked is False:
        STOP_OPTIONS_ARRAY.append('cozgu')
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device exited cozgu-status')
    # COZGU SWITCH --------------
    # ---------------------------


def check_ariza():
    """ Description """
    global OPTIONS_CHANGED
    # ARIZA SWITCH ##############
    # ###########################
    btn_ariza_checked = BTN_ARIZA.check_switch()
    if btn_ariza_checked is True:
        if 'ariza' in STOP_OPTIONS_ARRAY:
            STOP_OPTIONS_ARRAY.remove('ariza')
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device exited azriza-status')
    elif btn_ariza_checked is False:
        STOP_OPTIONS_ARRAY.append('ariza')
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device exited ariza-status')
    # ARIZA SWITCH --------------
    # ---------------------------


def check_ayar():
    """ Description """
    global OPTIONS_CHANGED
    # AYAR SWITCH ###############
    # ###########################
    btn_ayar_checked = BTN_AYAR.check_switch()
    if btn_ayar_checked is True:
        if 'ayar' in STOP_OPTIONS_ARRAY:
            STOP_OPTIONS_ARRAY.remove('ayar')
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device exited ayar-status')
    elif btn_ayar_checked is False:
        STOP_OPTIONS_ARRAY.append('ayar')
        OPTIONS_CHANGED = 1
        LOGGING.log_info('Device exited ayar-status')
    # AYAR SWITCH ---------------
    # ---------------------------


def gpio_check():
    """ Description """
    global OPTIONS_CHANGED, STOP_OPTIONS_ARRAY

    OPTIONS_CHANGED = 0

    check_kapali()

    # if SYSTEM_ON == 1:
    #     check_start_stop()

    if MACHINE_START_STOP == 0 and SYSTEM_ON == 1:
        check_bobin()
        check_cozgu()
        check_ariza()
        check_ayar()

    if STOP_OPTIONS_ARRAY:
        LCD.refresh_lcd(STOP_OPTIONS_ARRAY[len(STOP_OPTIONS_ARRAY) - 1], COUNTER_NR)

    if OPTIONS_CHANGED == 1 and STOP_OPTIONS_ARRAY:
        JSON_FUNCS.change_json(what=STOP_OPTIONS_ARRAY[len(STOP_OPTIONS_ARRAY) - 1])


def event_start_stop(channel):
    """ Description """
    global MACHINE_START_STOP, OPTIONS_CHANGED
    # START/STOP SWITCH ##############
    # ################################
    # start stop und nebenarbeiten an der maschine
    # wenn start switch on, zeigt nur start bzw. calisiyor
    if SYSTEM_ON == 1:
        btn_start_stop_checked = BTN_START_STOP.check_switch_once()
        if btn_start_stop_checked is True:
            if 'stop' in STOP_OPTIONS_ARRAY:
                STOP_OPTIONS_ARRAY.remove('stop')
            STOP_OPTIONS_ARRAY.append('start')
            MACHINE_START_STOP = 1
            OPTIONS_CHANGED = 1
            run_time.start_time()
            LOGGING.log_info('Device started')
        # maschiene gestopt
        # zusatzlich kann signalisiert werden, warum die maschine gestopt
        elif btn_start_stop_checked is False:
            if 'start' in STOP_OPTIONS_ARRAY:
                STOP_OPTIONS_ARRAY.remove('start')
            STOP_OPTIONS_ARRAY.append('stop')
            MACHINE_START_STOP = 0
            OPTIONS_CHANGED = 1
            run_time.stop_time()
            LOGGING.log_info('Device stopped')

    LOGGING.log_info(channel)
    # START/STOP SWITCH --------
    # ---------------------------


def event_counter(channel):
    """ Description """
    global COUNTER_NR, MACHINE_START_STOP, OPTIONS_CHANGED

    if SYSTEM_ON == 1:
        # sleep(0.1)
        btn_start_stop_checked_cnt = BTN_START_STOP.check_switch_once()
        if btn_start_stop_checked_cnt is True:
            COUNTER_NR = COUNTER_NR + 1
            JSON_FUNCS.change_json(what='counter', state=[COUNTER_NR, run_time.get_run_time()])
            # JSON_FUNCS.change_json(what='counter', state=[COUNTER_NR, None])
            OPTIONS_CHANGED = 1
            LOGGING.log_info(channel)


def event_reset(channel):
    """ Description """
    global COUNTER_NR, MACHINE_START_STOP, SYSTEM_ON, OPTIONS_CHANGED

    if MACHINE_START_STOP == 0:
        sleep(0.5)
        btn_start_stop_checked_rst = BTN_START_STOP.check_switch_once()
        if btn_start_stop_checked_rst is False:
            COUNTER_NR = 0
            JSON_FUNCS.change_json(what='reset')
            JSON_FUNCS.change_json(what='counter', state=0)
            OPTIONS_CHANGED = 1
            LOGGING.log_info('Counter reset')
            LOGGING.log_info(channel)


def loop():
    """ Description """

    LOGGING.log_info('gpio_check loop begins.')
    while True:
        gpio_check()
        sleep(0.2)


def add_events():
    """ Description """
    check_kapali()
    event_start_stop(None)
    BTN_START_STOP.add_callback(mode='both', callback=event_start_stop)
    BTN_COUNTER.add_callback(mode='rising', callback=event_counter)
    BTN_RESET.add_callback(mode='rising', callback=event_reset)


if __name__ == '__main__':

    LOGGING.log_info('System loaded.')
    try:
        add_events()
        loop()
        classes.gpio_cleanup()

    except (KeyboardInterrupt, SystemExit):
        print('keyboard interrupt detected')
        LOGGING.log_info('System stopped.')
        classes.gpio_cleanup()
        LCD.lcd_close()
    # end of program
    # ##############
