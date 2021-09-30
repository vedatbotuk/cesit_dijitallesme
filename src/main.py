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
TOTAL_COUNTER = JSON_FUNCS.get_total_counter()

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

RUN_TIME = classes.StartStopWatch()

KEYPAD_INSTALL = CONFIG_JSON['module']['keypad']['install']
if KEYPAD_INSTALL is True:
    KEY_PAD = classes.KeyPad()
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


def gpio_check_start():
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
        STOP_OPTIONS_ARRAY

    # AC/KAPA SWITCH
    # ###########################
    btn_kapali_checked_once = BTN_KAPALI.check_switch_once()
    if btn_kapali_checked_once is True:
        STOP_OPTIONS_ARRAY.append('kapali')
        SYSTEM_ON = 0
        LOGGING.log_info('Program Start - Device off')
    elif btn_kapali_checked_once is False:
        STOP_OPTIONS_ARRAY.append('stop')
        SYSTEM_ON = 1
        LOGGING.log_info('Program Start - Device on')
    # AC/KAPA SWITCH ------------
    # ---------------------------

    # START/STOP SWITCH ##############
    # ################################
    # start stop und nebenarbeiten an der maschine
    # wenn start switch on, zeigt nur start bzw. calisiyor
    btn_start_stop_checked_once = BTN_START_STOP.check_switch_once()
    if btn_start_stop_checked_once is True:
        MACHINE_START_STOP = 1
        LOGGING.log_info('Program Start - Device started')
        LCD.refresh_lcd('stop', COUNTER_NR)
    # maschiene gestopt
    # zusatzlich kann signalisiert werden, warum die maschine gestopt
    elif btn_start_stop_checked_once is False:
        MACHINE_START_STOP = 0
        LOGGING.log_info('Program Start - Device stopped')
        LCD.refresh_lcd('kapali', COUNTER_NR)

    # START/STOP SWITCH --------
    # ---------------------------

    # BOBIN SWITCH ##############
    # ###########################
    # ab hier testet alle nebenarbeiten an der maschine
    btn_bobin_checked_once = BTN_BOBIN.check_switch_once()
    if btn_bobin_checked_once is True:
        LOGGING.log_info('Program Start - Device exited bobin-status')
    elif btn_bobin_checked_once is False:
        LOGGING.log_info('Program Start - Device at bobin-status')
    # BOBIN SWITCH --------------
    # ---------------------------

    # COZGU SWITCH ##############
    # ###########################
    btn_cozgu_checked_once = BTN_COZGU.check_switch_once()
    if btn_cozgu_checked_once is True:
        LOGGING.log_info('Program Start - Device exited cozgu-status')
    elif btn_cozgu_checked_once is False:
        LOGGING.log_info('Program Start - Device at cozgu-status')
    # COZGU SWITCH --------------
    # ---------------------------

    # ARIZA SWITCH ##############
    # ###########################
    btn_ariza_checked_once = BTN_ARIZA.check_switch_once()
    if btn_ariza_checked_once is True:
        LOGGING.log_info('Program Start - Device exited azriza-status')
    elif btn_ariza_checked_once is False:
        LOGGING.log_info('Program Start - Device at ariza-status')
    # ARIZA SWITCH --------------
    # ---------------------------

    # AYAR SWITCH ###############
    # ###########################
    btn_ayar_checked_once = BTN_AYAR.check_switch_once()
    if btn_ayar_checked_once is True:
        LOGGING.log_info('Program Start - Device exited ayar-status')
    elif btn_ayar_checked_once is False:
        LOGGING.log_info('Program Start - Device at ayar-status')
    # AYAR SWITCH ---------------
    # ---------------------------


def check_keypad():
    global TOTAL_COUNTER, COUNTER_NR

    if KEYPAD_INSTALL is True:
        # button_to_give_counter = KEY_PAD.check_button('#')
        if KEY_PAD.check_button('#') is True:

            given_number = ''

            while True:
                get_button = str(KEY_PAD.get_given())
                if get_button == 'C':
                    break
                elif get_button == 'D':
                    given_number = ''
                elif get_button == '*':
                    try:
                        LCD.refresh_lcd('successfully', given_number)
                        print('given_number= ' + given_number)
                        TOTAL_COUNTER = int(given_number)
                        print('TOTAL_COUNTER= ' + str(TOTAL_COUNTER))
                    except Exception as e:
                        COUNTER_NR = 0
                        print(e)
                        LOGGING.log_info(e)
                    JSON_FUNCS.change_json(what='Given_Counter', state=TOTAL_COUNTER)

                    break
                else:
                    given_number = given_number + get_button
                    LCD.refresh_lcd('Given_Counter', given_number)

                sleep(0.2)


def show_remainder_counter():
    global TOTAL_COUNTER, COUNTER_NR

    if KEYPAD_INSTALL is True:
        if KEY_PAD.check_button('A') is True:
            LCD.refresh_lcd(what='show_remainder', state=TOTAL_COUNTER-COUNTER_NR)
            sleep(3)


def gpio_check():
    """ Description """
    global OPTIONS_CHANGED, STOP_OPTIONS_ARRAY, TOTAL_COUNTER, COUNTER_NR

    OPTIONS_CHANGED = 0

    check_kapali()

    show_remainder_counter()

    # if SYSTEM_ON == 1:
    #     check_start_stop()

    if MACHINE_START_STOP == 0 and SYSTEM_ON == 1:

        check_keypad()

        check_bobin()
        check_cozgu()
        check_ariza()
        check_ayar()

    if STOP_OPTIONS_ARRAY:
        LCD.refresh_lcd(STOP_OPTIONS_ARRAY[len(STOP_OPTIONS_ARRAY) - 1], COUNTER_NR)
        JSON_FUNCS.change_json(what=STOP_OPTIONS_ARRAY[len(STOP_OPTIONS_ARRAY) - 1])


def event_start_stop(channel):
    """ Description """
    global MACHINE_START_STOP, OPTIONS_CHANGED
    # START/STOP SWITCH ##############
    # ################################
    # start stop und nebenarbeiten an der maschine
    # wenn start switch on, zeigt nur start bzw. calisiyor
    if SYSTEM_ON == 1 and MACHINE_START_STOP == 0:
        btn_start_stop_checked = BTN_START_STOP.check_switch_once()
        if btn_start_stop_checked is True:
            if 'stop' in STOP_OPTIONS_ARRAY:
                STOP_OPTIONS_ARRAY.remove('stop')
            STOP_OPTIONS_ARRAY.append('start')
            MACHINE_START_STOP = 1
            OPTIONS_CHANGED = 1
            RUN_TIME.start()
            LOGGING.log_info('Device started')
        # maschiene gestopt
        # zusatzlich kann signalisiert werden, warum die maschine gestopt
        elif btn_start_stop_checked is False and MACHINE_START_STOP ==1:
            if 'start' in STOP_OPTIONS_ARRAY:
                STOP_OPTIONS_ARRAY.remove('start')
            STOP_OPTIONS_ARRAY.append('stop')
            MACHINE_START_STOP = 0
            OPTIONS_CHANGED = 1
            RUN_TIME.stop()
            LOGGING.log_info('Device stopped')

    LOGGING.log_info(channel)
    # START/STOP SWITCH --------
    # ---------------------------


def event_counter(channel):
    """ Description """
    global COUNTER_NR, MACHINE_START_STOP, OPTIONS_CHANGED, TOTAL_COUNTER

    # TODO: nach start zahlt der Counter + 1

    if SYSTEM_ON == 1 and MACHINE_START_STOP == 1:
        # sleep(0.1)
        cnt = 0
        for x in range(0, 5):
            btn_start_stop_checked_cnt = BTN_START_STOP.check_switch_once()
            if btn_start_stop_checked_cnt is True:
                cnt = cnt + 1

        if cnt == 5 and MACHINE_START_STOP == 1:
            COUNTER_NR = COUNTER_NR + 1
            JSON_FUNCS.change_json(what='counter', state=[COUNTER_NR, RUN_TIME.get_run_time()])
            # JSON_FUNCS.change_json(what='counter', state=[COUNTER_NR, None])
            OPTIONS_CHANGED = 1
            LOGGING.log_info(channel)


def event_reset(channel):
    """ Description """
    global COUNTER_NR, MACHINE_START_STOP, SYSTEM_ON, OPTIONS_CHANGED

    if MACHINE_START_STOP == 0:
        sleep(0.25)
        btn_start_stop_checked_rst = BTN_START_STOP.check_switch_once()
        if btn_start_stop_checked_rst is False:
            sleep(0.25)
            btn_start_stop_checked_rst = BTN_RESET.check_switch_once()
            if btn_start_stop_checked_rst is True:
                COUNTER_NR = 0
                RUN_TIME.reset_time()
                LCD.refresh_lcd(what='reset', state=None)
                JSON_FUNCS.change_json(what='reset')
                JSON_FUNCS.change_json(what='counter', state=[0, 1])
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
    # check_kapali()
    # btn_kapali_checked_start = BTN_KAPALI.check_switch_once()
    # if btn_kapali_checked_start is False:
    #     event_start_stop(None)
    BTN_START_STOP.add_callback(mode='both', callback=event_start_stop)
    BTN_COUNTER.add_callback(mode='rising', callback=event_counter)
    BTN_RESET.add_callback(mode='rising', callback=event_reset)


if __name__ == '__main__':

    LOGGING.log_info('System loaded.')
    try:
        gpio_check_start()
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
