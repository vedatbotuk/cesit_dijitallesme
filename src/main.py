#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

# #######
# Imports
from time import sleep
import classes
from classes import os_commands

# #####
# Setup
CONFIG_JSON = classes.get_setup()

LOGGING = classes.LogInfo(CONFIG_JSON['main']['log'],
                          CONFIG_JSON['main']['log_level'],
                          CONFIG_JSON['main']['log_path'])

LOGGING.log_info('--- System starting ---')

MACHINE_START = 0
SYSTEM_ON = 0
STATUS_CHANGED = 1
COUNTER_CHANGED = 1
COUNTER_PUSHED = 0
RESET_PUSHED = 0
RESET_CHANGED = 0

# TODO: überlege eine bessere Lösung
STATUS_ARRAY = []

JSON_FUNCS = classes.JsonFuncs()
COUNTER_NR = JSON_FUNCS.get_counter()
TOTAL_COUNTER = JSON_FUNCS.get_total_counter()

SAVED_PRODUCTIVE_RUN_TIME = JSON_FUNCS.get_saved_productive_run_time()
SAVED_BOBIN_TIME = JSON_FUNCS.get_saved_bobin_time()
SAVED_ARIZA_TIME = JSON_FUNCS.get_saved_ariza_time()
SAVED_COZGU_TIME = JSON_FUNCS.get_saved_cozgu_time()
SAVED_AYAR_TIME = JSON_FUNCS.get_saved_ayar_time()

PRODUCTIVE_RUN_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_PRODUCTIVE_RUN_TIME)
BOBIN_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_BOBIN_TIME)
ARIZA_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_ARIZA_TIME)
COZGU_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_COZGU_TIME)
AYAR_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_AYAR_TIME)

# PRODUCTIVE_RUN_TIME = PRODUCTIVE_RUN_TIME_WATCH.get_calculated_total_time()
# BOBIN_TIME = BOBIN_TIME_WATCH.get_calculated_total_time()
# ARIZA_TIME = ARIZA_TIME_WATCH.get_calculated_total_time()
# COZGU_TIME = COZGU_TIME_WATCH.get_calculated_total_time()
# AYAR_TIME = AYAR_TIME_WATCH.get_calculated_total_time()

PRODUCTIVE_RUN_TIME = 0
BOBIN_TIME = 0
ARIZA_TIME = 0
COZGU_TIME = 0
AYAR_TIME = 0
TOTAL_TIME = 0

TIME_BTW_COUNTER = 0

LCD = classes.LcdModule()
BTN_KAPALI = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_kapali'])
BTN_KAPALI.add_switches()
BTN_START_STOP = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_start_stop'])
BTN_START_STOP.add_switches()
BTN_STOP = classes.ButtonSwitch(CONFIG_JSON['switches']['btn_start_stop'])
BTN_STOP.add_switches()
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

KEYPAD_INSTALL = CONFIG_JSON['module']['keypad']['install']
if KEYPAD_INSTALL is True:
    KEY_PAD = classes.KeyPad()


# end of setup
# ############


def check_kapali():
    """ Description """
    global SYSTEM_ON, STATUS_CHANGED
    # AC/KAPA SWITCH
    # ###########################
    btn_kapali_checked = BTN_KAPALI.check_switch()
    if btn_kapali_checked is True:
        STATUS_ARRAY.append('kapali')
        if 'stop' in STATUS_ARRAY:
            STATUS_ARRAY.remove('stop')
        SYSTEM_ON = 0
        STATUS_CHANGED = 1
        LOGGING.log_info('Device off')
    elif btn_kapali_checked is False:
        if 'kapali' in STATUS_ARRAY:
            STATUS_ARRAY.remove('kapali')
        STATUS_ARRAY.append('stop')
        SYSTEM_ON = 1
        STATUS_CHANGED = 1
        LOGGING.log_info('Device on')
    # AC/KAPA SWITCH ------------
    # ---------------------------


def check_start_stop():
    global MACHINE_START, COUNTER_NR, STATUS_CHANGED, PRODUCTIVE_RUN_TIME

    # START/STOP SWITCH ##############
    # ################################
    # start stop und nebenarbeiten an der maschine
    # wenn start switch on, zeigt nur start bzw. calisiyor
    btn_start_stop_checked = BTN_START_STOP.check_switch()
    if btn_start_stop_checked is True:
        if 'stop' in STATUS_ARRAY:
            STATUS_ARRAY.remove('stop')
        STATUS_ARRAY.append('start')
        MACHINE_START = 1
        STATUS_CHANGED = 1
        PRODUCTIVE_RUN_TIME_WATCH.stop()
        PRODUCTIVE_RUN_TIME = PRODUCTIVE_RUN_TIME_WATCH.get_calculated_total_time()
        LOGGING.log_info('Device started')
    # maschiene gestopt
    # zusatzlich kann signalisiert werden, warum die maschine gestopt
    elif btn_start_stop_checked is False:
        if 'start' in STATUS_ARRAY:
            STATUS_ARRAY.remove('start')
        STATUS_ARRAY.append('stop')
        MACHINE_START = 0
        STATUS_CHANGED = 1
        PRODUCTIVE_RUN_TIME_WATCH.start()
        LOGGING.log_info('Device stopped')
    # START/STOP SWITCH --------
    # ---------------------------


def check_bobin():
    """ Description """
    global STATUS_CHANGED, BOBIN_TIME
    # BOBIN SWITCH ##############
    # ###########################
    # ab hier testet alle nebenarbeiten an der maschine
    btn_bobin_checked = BTN_BOBIN.check_switch()
    if btn_bobin_checked is False:
        if 'bobin' in STATUS_ARRAY[len(STATUS_ARRAY) - 1]:
            STATUS_ARRAY.remove('bobin')
            BOBIN_TIME_WATCH.stop()
            BOBIN_TIME = BOBIN_TIME_WATCH.get_calculated_total_time()
        STATUS_CHANGED = 1
        LOGGING.log_info('Device exited bobin-status')
    elif btn_bobin_checked is True:
        STATUS_ARRAY.append('bobin')
        STATUS_CHANGED = 1
        BOBIN_TIME_WATCH.start()
        LOGGING.log_info('Device at bobin-status')
    # BOBIN SWITCH --------------
    # ---------------------------


def check_cozgu():
    """ Description """
    global STATUS_CHANGED, COZGU_TIME
    # COZGU SWITCH ##############
    # ###########################
    btn_cozgu_checked = BTN_COZGU.check_switch()
    if btn_cozgu_checked is False:
        if 'cozgu' in STATUS_ARRAY[len(STATUS_ARRAY) - 1]:
            STATUS_ARRAY.remove('cozgu')
            COZGU_TIME_WATCH.stop()
            COZGU_TIME = COZGU_TIME_WATCH.get_calculated_total_time()
        STATUS_CHANGED = 1
        LOGGING.log_info('Device exited cozgu-status')
    elif btn_cozgu_checked is True:
        STATUS_ARRAY.append('cozgu')
        STATUS_CHANGED = 1
        COZGU_TIME_WATCH.start()
        LOGGING.log_info('Device at cozgu-status')
    # COZGU SWITCH --------------
    # ---------------------------


def check_ariza():
    """ Description """
    global STATUS_CHANGED, ARIZA_TIME
    # ARIZA SWITCH ##############
    # ###########################
    btn_ariza_checked = BTN_ARIZA.check_switch()
    if btn_ariza_checked is False:
        if 'ariza' in STATUS_ARRAY[len(STATUS_ARRAY) - 1]:
            STATUS_ARRAY.remove('ariza')
            ARIZA_TIME_WATCH.stop()
            ARIZA_TIME = ARIZA_TIME_WATCH.get_calculated_total_time()
        STATUS_CHANGED = 1
        LOGGING.log_info('Device exited azriza-status')
    elif btn_ariza_checked is True:
        STATUS_ARRAY.append('ariza')
        STATUS_CHANGED = 1
        ARIZA_TIME_WATCH.start()
        LOGGING.log_info('Device at ariza-status')
    # ARIZA SWITCH --------------
    # ---------------------------


def check_ayar():
    """ Description """
    global STATUS_CHANGED, AYAR_TIME
    # AYAR SWITCH ###############
    # ###########################
    btn_ayar_checked = BTN_AYAR.check_switch()
    if btn_ayar_checked is False:
        if 'ayar' in STATUS_ARRAY[len(STATUS_ARRAY) - 1]:
            STATUS_ARRAY.remove('ayar')
            AYAR_TIME_WATCH.stop()
            AYAR_TIME = AYAR_TIME_WATCH.get_calculated_total_time()
        STATUS_CHANGED = 1
        LOGGING.log_info('Device exited ayar-status')
    elif btn_ayar_checked is True:
        STATUS_ARRAY.append('ayar')
        STATUS_CHANGED = 1
        AYAR_TIME_WATCH.start()
        LOGGING.log_info('Device at ayar-status')
    # AYAR SWITCH ---------------
    # ---------------------------


def gpio_check_start_stop():
    """ Description """
    global MACHINE_START, STATUS_ARRAY, TOTAL_TIME

    check_kapali()
    JSON_FUNCS.change_json(what='counter', state=[COUNTER_NR, PRODUCTIVE_RUN_TIME, TIME_BTW_COUNTER, TOTAL_TIME])

    # TODO: Beim Start 0,7 Sekunde Verzögerung bei der Status angezeigt.
    if SYSTEM_ON == 1:
        check_start_stop()
        if MACHINE_START == 0:
            check_bobin()
            check_cozgu()
            check_ariza()
            check_ayar()


def given_counter():
    """ Description """
    return_number = None
    given_number = ''

    LCD.refresh_lcd('Given_Counter', given_number)

    while True:
        get_button = str(KEY_PAD.check_button())
        if get_button == 'C':
            break

        elif get_button == 'D':
            given_number = given_number[:-1]
            LCD.refresh_lcd('Given_Counter', given_number)

        elif get_button == '*':
            try:
                return_number = int(given_number)

                LCD.refresh_lcd('successfully', given_number)
                sleep(2)
                break

            except Exception as e:
                LCD.refresh_lcd('Counter_not_allowed')
                sleep(2)
                LCD.refresh_lcd('Given_Counter', given_number)
                return_number = None
                LOGGING.log_info(e)

        elif get_button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            given_number = given_number + get_button
            LCD.refresh_lcd('Given_Counter', given_number)

        sleep(0.2)

    return return_number


def keypad_give_total_counter():
    """ Description """
    global TOTAL_COUNTER, COUNTER_NR

    if KEYPAD_INSTALL is True:
        wait = 15
        checked = 0
        for cnt in range(0, wait):
            button_to_give_counter = KEY_PAD.check_button()
            if button_to_give_counter == "#":
                checked = checked + 1
            else:
                break
            sleep(0.2)

        if checked == wait:
            total_counter = given_counter()
            if total_counter is not None:
                TOTAL_COUNTER = total_counter
                JSON_FUNCS.change_json(what='Given_Total_Counter', state=TOTAL_COUNTER)
        else:
            pass


def keypad_give_os_cmd():
    """ Description """
    global COUNTER_NR

    if KEYPAD_INSTALL is True:
        wait = 15
        checked = 0
        for cnt in range(0, wait):
            button_to_give_total = KEY_PAD.check_button()
            if button_to_give_total == "D":
                checked = checked + 1
            else:
                break
            sleep(0.2)

        if checked == wait:
            given_code = ''
            LCD.refresh_lcd('Given_Code', given_code)

            while True:
                get_button = str(KEY_PAD.check_button())
                if get_button == 'C':
                    break

                elif get_button == 'D':
                    given_code = given_code[:-1]
                    LCD.refresh_lcd('Given_Code', given_code)

                elif get_button == '*':

                    if given_code == '100':
                        os_commands.shutdown_system()
                        LCD.lcd_close()
                        exit()
                        break

                    elif given_code == '101':
                        os_commands.reboot_system()
                        LCD.lcd_close()
                        exit()
                        break

                    elif given_code == '102':
                        os_commands.restart_program()
                        LCD.lcd_close()
                        exit()
                        break

                    elif given_code == '103':
                        os_commands.update_code()
                        LCD.lcd_close()
                        break

                    elif given_code == '104':
                        change_counter = given_counter()
                        if change_counter is not None:
                            COUNTER_NR = change_counter
                            JSON_FUNCS.change_json(what='Given_Counter', state=COUNTER_NR)
                        break

                    else:
                        LCD.refresh_lcd('Code_not_exists')
                        sleep(2)
                        given_code = ''
                        LCD.refresh_lcd('Given_Code', given_code)

                elif get_button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    given_code = given_code + get_button
                    LCD.refresh_lcd('Given_Code', given_code)

                sleep(0.2)


def show_total_counter():
    """ Description """
    global TOTAL_COUNTER, COUNTER_NR

    if KEYPAD_INSTALL is True:
        while True:
            button_to_give_total = KEY_PAD.check_button()
            if button_to_give_total == 'A':
                LCD.refresh_lcd(what='show_total', state=TOTAL_COUNTER)
            else:
                break
            sleep(0.5)


def show_remainder_counter():
    """ Description """
    global TOTAL_COUNTER, COUNTER_NR

    if KEYPAD_INSTALL is True:
        while True:
            button_to_give_remainder = KEY_PAD.check_button()
            if button_to_give_remainder == 'B':
                LCD.refresh_lcd(what='show_remainder', state=TOTAL_COUNTER - COUNTER_NR)
            else:
                break
            sleep(0.5)


def clear_lcd():
    """ If LCD shows not Correct, with this function could be refreshed. """

    if KEYPAD_INSTALL is True:
        if KEY_PAD.check_button() == "C":
            wait = 15
            checked = 0
            for cnt in range(0, wait):
                button_to_give_total = KEY_PAD.check_button()
                if button_to_give_total == "C":
                    checked = checked + 1
                else:
                    break
                sleep(0.2)

            if checked == wait:
                LCD.lcd_clear()
                sleep(0.25)
                LCD.refresh_lcd(what='after_clear')
                sleep(0.25)


def update_cycle():
    global PRODUCTIVE_RUN_TIME, BOBIN_TIME, ARIZA_TIME, COZGU_TIME, AYAR_TIME

    JSON_FUNCS.change_json(what='write_status_times',
                           state=[PRODUCTIVE_RUN_TIME, BOBIN_TIME, ARIZA_TIME, COZGU_TIME, AYAR_TIME])


def gpio_check():
    """ Description """
    global STATUS_CHANGED, STATUS_ARRAY, TOTAL_COUNTER, COUNTER_NR, COUNTER_CHANGED, RESET_CHANGED, \
        PRODUCTIVE_RUN_TIME, TOTAL_TIME

    check_kapali()
    check_start_stop()

    show_remainder_counter()
    show_total_counter()
    clear_lcd()

    # if STATUS_ARRAY:
    LCD.refresh_lcd(STATUS_ARRAY[len(STATUS_ARRAY) - 1], COUNTER_NR)

    if MACHINE_START == 0:
        keypad_give_total_counter()
        keypad_give_os_cmd()

        check_bobin()
        check_cozgu()
        check_ariza()
        check_ayar()

        reset_check()

    if STATUS_CHANGED == 1:
        JSON_FUNCS.change_json(what=STATUS_ARRAY[len(STATUS_ARRAY) - 1])
        update_cycle()
        STATUS_CHANGED = 0

    if COUNTER_CHANGED == 1:
        JSON_FUNCS.change_json(what='counter', state=[COUNTER_NR, PRODUCTIVE_RUN_TIME, TIME_BTW_COUNTER, TOTAL_TIME])
        COUNTER_CHANGED = 0

    if RESET_CHANGED == 1:
        update_cycle()
        LCD.refresh_lcd(what='reset')
        JSON_FUNCS.change_json(what='reset')
        JSON_FUNCS.change_json(what='counter', state=[0, 0, 0, 0])
        RESET_CHANGED = 0


# def event_start_stop(channel):
#     """ Description """
#     global COUNTER_NR, COUNTER_CHANGED, MACHINE_START, STATUS_CHANGED
#
#     # START/STOP SWITCH ##############
#     # ################################
#     btn_start_stop_chk = BTN_START_STOP.check_switch_once()
#     if btn_start_stop_chk is True and MACHINE_START == 0:
#         # if BTN_START_STOP.check_five_times(True) is True:
#         # if 'stop' in STATUS_ARRAY:
#         #     STATUS_ARRAY.remove('stop')
#         STATUS_ARRAY.append('start')
#         MACHINE_START = 1
#         STATUS_CHANGED = 1  # for refresh LCD
#         PRODUCTIVE_RUN_TIME_WATCH.start()
#         LOGGING.log_info('')
#         LOGGING.log_info(str(channel) + ' Device started')
#
#     elif btn_start_stop_chk is False and MACHINE_START == 1:
#         # if BTN_START_STOP.check_five_times(True) is False:
#         # if 'start' in STATUS_ARRAY:
#         #     STATUS_ARRAY.remove('start')
#         STATUS_ARRAY.append('stop')
#         MACHINE_START = 0
#         STATUS_CHANGED = 1  # for refresh LCD
#         PRODUCTIVE_RUN_TIME_WATCH.stop()
#         LOGGING.log_info(str(channel) + ' Device stopped')
#         LOGGING.log_info('')
#     # START/STOP SWITCH --------


def event_counter(channel):
    """ Description """
    global COUNTER_NR, COUNTER_CHANGED, PRODUCTIVE_RUN_TIME, BOBIN_TIME, ARIZA_TIME, COZGU_TIME, AYAR_TIME,\
        TOTAL_TIME, COUNTER_PUSHED, TIME_BTW_COUNTER

    btn_cnt = BTN_COUNTER.check_switch_once()
    if btn_cnt is True:
        COUNTER_PUSHED = 1
        # LOGGING.log_info('')
        # LOGGING.log_info(str(channel) + ' high')

    elif btn_cnt is False:
        if COUNTER_PUSHED == 1:
            COUNTER_NR = COUNTER_NR + 1
            PRODUCTIVE_RUN_TIME = PRODUCTIVE_RUN_TIME_WATCH.get_calculated_total_time()
            TOTAL_TIME = PRODUCTIVE_RUN_TIME + BOBIN_TIME + AYAR_TIME + COZGU_TIME + AYAR_TIME
            TIME_BTW_COUNTER = PRODUCTIVE_RUN_TIME_WATCH.get_counter_time()
            COUNTER_CHANGED = 1  # for refresh JSON
            COUNTER_PUSHED = 0
            # LOGGING.log_info(str(channel) + ' ' + str(COUNTER_NR))
        # LOGGING.log_info(str(channel) + ' low')
        # LOGGING.log_info('')
        else:
            LOGGING.log_info('Wrong signal -> Counter was not pushed ' + str(channel))


# def event_reset(channel):
#     """ Description """
#     global COUNTER_NR, MACHINE_START, RESET_CHANGED, RESET_PUSHED
#
#     btn_rest = BTN_RESET.check_switch_once()
#     if btn_rest is True:
#         RESET_PUSHED = 1
#
#     elif btn_rest is False:
#         if MACHINE_START == 0 and RESET_PUSHED == 1:
#             COUNTER_NR = 0
#
#             PRODUCTIVE_RUN_TIME_WATCH.reset_time()
#             BOBIN_TIME_WATCH.reset_time()
#             ARIZA_TIME_WATCH.reset_time()
#             COZGU_TIME_WATCH.reset_time()
#             ARIZA_TIME_WATCH.reset_time()
#
#             RESET_CHANGED = 1
#             RESET_PUSHED = 0
#             LOGGING.log_info('Counter reset')
#             # LOGGING.log_info(channel)
#         else:
#             LOGGING.log_info('Wrong signal -> Reset was not pushed ' + str(channel))


def reset_check():
    """ Description """
    global COUNTER_NR, RESET_CHANGED, RESET_PUSHED, PRODUCTIVE_RUN_TIME, BOBIN_TIME,\
        ARIZA_TIME, COZGU_TIME, AYAR_TIME, TOTAL_TIME

    btn_rest = BTN_RESET.check_switch_once()
    if btn_rest is True:
        sleep(0.1)
        btn_rest = BTN_RESET.check_switch_once()
        if btn_rest is True:
            sleep(0.4)
            btn_rest = BTN_RESET.check_switch_once()
            if btn_rest is True:
                RESET_PUSHED = 1

    if RESET_PUSHED == 1:
        COUNTER_NR = 0

        PRODUCTIVE_RUN_TIME_WATCH.reset_time()
        BOBIN_TIME_WATCH.reset_time()
        ARIZA_TIME_WATCH.reset_time()
        COZGU_TIME_WATCH.reset_time()
        AYAR_TIME_WATCH.reset_time()

        PRODUCTIVE_RUN_TIME = 0
        BOBIN_TIME = 0
        ARIZA_TIME = 0
        COZGU_TIME = 0
        AYAR_TIME = 0
        TOTAL_TIME = 0

        RESET_CHANGED = 1
        RESET_PUSHED = 0
        LOGGING.log_info('Counter reset')


def loop():
    """ Description """

    LOGGING.log_info('gpio_check loop begins.')
    while True:
        gpio_check()
        sleep(0.2)


def add_events():
    """ Description """
    # BTN_START_STOP.add_callback(mode='both', callback=event_start_stop)
    BTN_COUNTER.add_callback(mode='both', callback=event_counter)
    # BTN_RESET.add_callback(mode='both', callback=event_reset)


if __name__ == '__main__':

    LOGGING.log_info('System loaded.')
    try:
        add_events()
        gpio_check_start_stop()
        loop()

    except (KeyboardInterrupt, SystemExit):
        print('keyboard interrupt detected')
        LOGGING.log_info('System stopped.')
        classes.gpio_cleanup()
        LCD.lcd_close()
    # end of program
    # ##############
