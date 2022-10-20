#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

# #######
# Imports
from time import sleep
import classes
from classes import os_commands
import concurrent.futures

is_shutdown = False

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

SAVED_TOTAL_TIME = JSON_FUNCS.get_saved_total_time()
SAVED_PRODUCTIVE_RUN_TIME = JSON_FUNCS.get_saved_productive_run_time()
SAVED_STOP_TIME = JSON_FUNCS.get_saved_stop_time()
SAVED_BOBIN_TIME = JSON_FUNCS.get_saved_bobin_time()
SAVED_ARIZA_TIME = JSON_FUNCS.get_saved_ariza_time()
SAVED_COZGU_TIME = JSON_FUNCS.get_saved_cozgu_time()
SAVED_AYAR_TIME = JSON_FUNCS.get_saved_ayar_time()

TOTAL_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_TOTAL_TIME)
PRODUCTIVE_RUN_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_PRODUCTIVE_RUN_TIME)
STOP_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_STOP_TIME)
BOBIN_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_BOBIN_TIME)
ARIZA_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_ARIZA_TIME)
COZGU_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_COZGU_TIME)
AYAR_TIME_WATCH = classes.StartStopWatch(saved_run_time=SAVED_AYAR_TIME)


PRODUCTIVE_RUN_TIME = 0
STOP_TIME = 0
BOBIN_TIME = 0
ARIZA_TIME = 0
COZGU_TIME = 0
AYAR_TIME = 0
TOTAL_TIME = 0

TIME_BTW_COUNTER = 0

CHECK_MINUTE = ''

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
    global SYSTEM_ON, STATUS_CHANGED, TOTAL_TIME
    # AC/KAPA SWITCH
    # ###########################
    btn_kapali_checked = BTN_KAPALI.check_switch()
    if btn_kapali_checked is True:
        STATUS_ARRAY.append('kapali')
        if 'stop' in STATUS_ARRAY:
            STATUS_ARRAY.remove('stop')
        TOTAL_TIME_WATCH.stop()
        SYSTEM_ON = 0
        STATUS_CHANGED = 1
        LOGGING.log_info('Device off')
    elif btn_kapali_checked is False:
        if 'kapali' in STATUS_ARRAY:
            STATUS_ARRAY.remove('kapali')
        TOTAL_TIME_WATCH.start()
        TOTAL_TIME = TOTAL_TIME_WATCH.get_calculated_total_time()
        STATUS_ARRAY.append('stop')
        SYSTEM_ON = 1
        STATUS_CHANGED = 1
        LOGGING.log_info('Device on')
    # AC/KAPA SWITCH ------------
    # ---------------------------


def check_start_stop():
    global MACHINE_START, COUNTER_NR, STATUS_CHANGED, PRODUCTIVE_RUN_TIME, STOP_TIME, CHECK_MINUTE

    # START/STOP SWITCH ##############
    # ################################
    # start stop und nebenarbeiten an der maschine
    # wenn start switch on, zeigt nur start bzw. calisiyor
    btn_start_stop_checked = BTN_START_STOP.check_switch()
    if btn_start_stop_checked is True:
        if 'stop' in STATUS_ARRAY:
            STATUS_ARRAY.remove('stop')
        PRODUCTIVE_RUN_TIME_WATCH.start()
        PRODUCTIVE_RUN_TIME = PRODUCTIVE_RUN_TIME_WATCH.get_calculated_total_time()
        STOP_TIME_WATCH.stop()
        STATUS_ARRAY.append('start')
        MACHINE_START = 1
        STATUS_CHANGED = 1
        LOGGING.log_info('Device started')
    # maschiene gestopt
    # zusatzlich kann signalisiert werden, warum die maschine gestopt
    elif btn_start_stop_checked is False:
        if 'start' in STATUS_ARRAY:
            STATUS_ARRAY.remove('start')
        PRODUCTIVE_RUN_TIME_WATCH.stop()
        STOP_TIME_WATCH.start()
        STATUS_ARRAY.append('stop')
        MACHINE_START = 0
        STATUS_CHANGED = 1
        LOGGING.log_info('Device stopped')

    if STATUS_ARRAY[len(STATUS_ARRAY) - 1] == 'stop':
        now_for_check_minute = classes.get_minute()
        if CHECK_MINUTE != now_for_check_minute:
            CHECK_MINUTE = now_for_check_minute
            STOP_TIME = STOP_TIME_WATCH.get_calculated_total_time()
            update_cycle()
    # START/STOP SWITCH --------
    # ---------------------------


def check_bobin():
    """ Description """
    global STATUS_CHANGED, BOBIN_TIME, STOP_TIME, CHECK_MINUTE
    # BOBIN SWITCH ##############
    # ###########################
    # ab hier testet alle nebenarbeiten an der maschine
    btn_bobin_checked = BTN_BOBIN.check_switch()
    if btn_bobin_checked is False:
        if 'bobin' in STATUS_ARRAY:
            STATUS_ARRAY.remove('bobin')
            BOBIN_TIME_WATCH.stop()
        STATUS_CHANGED = 1
        LOGGING.log_info('Device exited bobin-status')
    elif btn_bobin_checked is True:
        STATUS_ARRAY.append('bobin')
        STATUS_CHANGED = 1
        BOBIN_TIME_WATCH.start()
        STOP_TIME_WATCH.stop()
        STOP_TIME = STOP_TIME_WATCH.get_calculated_total_time()
        LOGGING.log_info('Device at bobin-status')

    if STATUS_ARRAY[len(STATUS_ARRAY) - 1] == 'bobin':
        now_for_check_minute = classes.get_minute()
        if CHECK_MINUTE != now_for_check_minute:
            CHECK_MINUTE = now_for_check_minute
            BOBIN_TIME = BOBIN_TIME_WATCH.get_calculated_total_time()
            update_cycle()
    # BOBIN SWITCH --------------
    # ---------------------------


def check_cozgu():
    """ Description """
    global STATUS_CHANGED, COZGU_TIME, STOP_TIME, CHECK_MINUTE
    # COZGU SWITCH ##############
    # ###########################
    btn_cozgu_checked = BTN_COZGU.check_switch()
    if btn_cozgu_checked is False:
        if 'cozgu' in STATUS_ARRAY:
            STATUS_ARRAY.remove('cozgu')
            COZGU_TIME_WATCH.stop()
        STATUS_CHANGED = 1
        LOGGING.log_info('Device exited cozgu-status')
    elif btn_cozgu_checked is True:
        STATUS_ARRAY.append('cozgu')
        STATUS_CHANGED = 1
        COZGU_TIME_WATCH.start()
        STOP_TIME_WATCH.stop()
        STOP_TIME = STOP_TIME_WATCH.get_calculated_total_time()
        LOGGING.log_info('Device at cozgu-status')

    if STATUS_ARRAY[len(STATUS_ARRAY) - 1] == 'cozgu':
        now_for_check_minute = classes.get_minute()
        if CHECK_MINUTE != now_for_check_minute:
            CHECK_MINUTE = now_for_check_minute
            COZGU_TIME = COZGU_TIME_WATCH.get_calculated_total_time()
            update_cycle()
    # COZGU SWITCH --------------
    # ---------------------------


def check_ariza():
    """ Description """
    global STATUS_CHANGED, ARIZA_TIME, STOP_TIME, CHECK_MINUTE
    # ARIZA SWITCH ##############
    # ###########################
    btn_ariza_checked = BTN_ARIZA.check_switch()
    if btn_ariza_checked is False:
        if 'ariza' in STATUS_ARRAY:
            STATUS_ARRAY.remove('ariza')
            ARIZA_TIME_WATCH.stop()
        STATUS_CHANGED = 1
        LOGGING.log_info('Device exited azriza-status')
    elif btn_ariza_checked is True:
        STATUS_ARRAY.append('ariza')
        STATUS_CHANGED = 1
        ARIZA_TIME_WATCH.start()
        STOP_TIME_WATCH.stop()
        STOP_TIME = STOP_TIME_WATCH.get_calculated_total_time()
        LOGGING.log_info('Device at ariza-status')

    if STATUS_ARRAY[len(STATUS_ARRAY) - 1] == 'ariza':
        now_for_check_minute = classes.get_minute()
        if CHECK_MINUTE != now_for_check_minute:
            CHECK_MINUTE = now_for_check_minute
            ARIZA_TIME = ARIZA_TIME_WATCH.get_calculated_total_time()
            update_cycle()
    # ARIZA SWITCH --------------
    # ---------------------------


def check_ayar():
    """ Description """
    global STATUS_CHANGED, AYAR_TIME, STOP_TIME, CHECK_MINUTE
    # AYAR SWITCH ###############
    # ###########################
    btn_ayar_checked = BTN_AYAR.check_switch()
    if btn_ayar_checked is False:
        if 'ayar' in STATUS_ARRAY:
            STATUS_ARRAY.remove('ayar')
            AYAR_TIME_WATCH.stop()
        STATUS_CHANGED = 1
        LOGGING.log_info('Device exited ayar-status')
    elif btn_ayar_checked is True:
        STATUS_ARRAY.append('ayar')
        STATUS_CHANGED = 1
        AYAR_TIME_WATCH.start()
        STOP_TIME_WATCH.stop()
        STOP_TIME = STOP_TIME_WATCH.get_calculated_total_time()
        LOGGING.log_info('Device at ayar-status')

    if STATUS_ARRAY[len(STATUS_ARRAY) - 1] == 'ayar':
        now_for_check_minute = classes.get_minute()
        if CHECK_MINUTE != now_for_check_minute:
            CHECK_MINUTE = now_for_check_minute
            AYAR_TIME = AYAR_TIME_WATCH.get_calculated_total_time()
            update_cycle()
    # AYAR SWITCH ---------------
    # ---------------------------


def gpio_check_start_stop():
    """ Description """
    global MACHINE_START, SYSTEM_ON, STATUS_ARRAY, TOTAL_TIME

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
    global TOTAL_TIME, PRODUCTIVE_RUN_TIME, STOP_TIME, BOBIN_TIME, ARIZA_TIME, COZGU_TIME, AYAR_TIME

    JSON_FUNCS.change_json(what='write_status_times',
                           state=[PRODUCTIVE_RUN_TIME, STOP_TIME, BOBIN_TIME, ARIZA_TIME, COZGU_TIME, AYAR_TIME, TOTAL_TIME])


def lcd_refresh(sleep_time):
    global STATUS_ARRAY, COUNTER_NR

    while not is_shutdown:
        show_remainder_counter()
        show_total_counter()
        clear_lcd()

        LCD.refresh_lcd(STATUS_ARRAY[len(STATUS_ARRAY) - 1], COUNTER_NR)
        sleep(sleep_time)


def json_refresh(sleep_time):
    global STATUS_ARRAY, COUNTER_NR, PRODUCTIVE_RUN_TIME, TIME_BTW_COUNTER, TOTAL_TIME

    while not is_shutdown:
        if STATUS_CHANGED == 1:
            JSON_FUNCS.change_json(what=STATUS_ARRAY[len(STATUS_ARRAY) - 1])
            JSON_FUNCS.change_json(what='write_status_times',
                                   state=[PRODUCTIVE_RUN_TIME, STOP_TIME, BOBIN_TIME, ARIZA_TIME, COZGU_TIME, AYAR_TIME,
                                          TOTAL_TIME])

        if COUNTER_CHANGED == 1:
            JSON_FUNCS.change_json(what='counter',
                                   state=[COUNTER_NR, PRODUCTIVE_RUN_TIME, TIME_BTW_COUNTER, TOTAL_TIME])

        if RESET_CHANGED == 1:
            JSON_FUNCS.change_json(what='reset')
            JSON_FUNCS.change_json(what='counter', state=[0, 0, 0, 0])
            JSON_FUNCS.change_json(what='write_status_times',
                                   state=[PRODUCTIVE_RUN_TIME, STOP_TIME, BOBIN_TIME, ARIZA_TIME, COZGU_TIME, AYAR_TIME,
                                          TOTAL_TIME])

        sleep(sleep_time)


def gpio_check():
    """ Description """
    global STATUS_CHANGED,SYSTEM_ON, STATUS_ARRAY, TOTAL_COUNTER, COUNTER_NR, COUNTER_CHANGED, RESET_CHANGED, \
        PRODUCTIVE_RUN_TIME, TOTAL_TIME

    check_kapali()

    if SYSTEM_ON == 1:
        check_start_stop()

    # if STATUS_ARRAY:
    # LCD.refresh_lcd(STATUS_ARRAY[len(STATUS_ARRAY) - 1], COUNTER_NR)

    if MACHINE_START == 0:
        keypad_give_total_counter()
        keypad_give_os_cmd()

        check_bobin()
        check_cozgu()
        check_ariza()
        check_ayar()

    if STATUS_CHANGED == 1:
        # JSON_FUNCS.change_json(what=STATUS_ARRAY[len(STATUS_ARRAY) - 1])
        update_cycle()
        STATUS_CHANGED = 0

    if COUNTER_CHANGED == 1:
        # JSON_FUNCS.change_json(what='counter', state=[COUNTER_NR, PRODUCTIVE_RUN_TIME, TIME_BTW_COUNTER, TOTAL_TIME])
        COUNTER_CHANGED = 0

    if RESET_CHANGED == 1:
        update_cycle()
        LCD.refresh_lcd(what='reset')
        # JSON_FUNCS.change_json(what='reset')
        # JSON_FUNCS.change_json(what='counter', state=[0, 0, 0, 0])
        RESET_CHANGED = 0


def event_counter(sleep_time):
    """ Description """
    global COUNTER_NR, COUNTER_CHANGED, PRODUCTIVE_RUN_TIME, TOTAL_TIME, COUNTER_PUSHED, TIME_BTW_COUNTER

    while not is_shutdown:
        # BTN_COUNTER.wait_for_rising()
        btn_cnt = BTN_COUNTER.check_switch_once()
        if btn_cnt is True:
            COUNTER_PUSHED = 1
            # LOGGING.log_info('')
            # LOGGING.log_info(str(channel) + ' high')

        elif btn_cnt is False and COUNTER_PUSHED == 1:
            COUNTER_NR = COUNTER_NR + 1
            PRODUCTIVE_RUN_TIME = PRODUCTIVE_RUN_TIME_WATCH.get_calculated_total_time()
            TOTAL_TIME = TOTAL_TIME_WATCH.get_calculated_total_time()
            TIME_BTW_COUNTER = PRODUCTIVE_RUN_TIME_WATCH.get_counter_time()
            COUNTER_CHANGED = 1  # for refresh JSON
            COUNTER_PUSHED = 0
            # LOGGING.log_info(str(COUNTER_NR))
            # LOGGING.log_info(' low')
            # LOGGING.log_info('')
        sleep(sleep_time)


def event_reset(sleep_time):
    """ Description """
    global COUNTER_NR, RESET_CHANGED, RESET_PUSHED, PRODUCTIVE_RUN_TIME, STOP_TIME, BOBIN_TIME,\
        ARIZA_TIME, COZGU_TIME, AYAR_TIME, TOTAL_TIME

    while not is_shutdown:
        # BTN_RESET.wait_for_rising()
        btn_rest = BTN_RESET.check_switch_once()
        if btn_rest is True:
            sleep(0.5)
            btn_rest = BTN_RESET.check_switch_once()
            if btn_rest is True:
                RESET_PUSHED = 1

        if RESET_PUSHED == 1:
            COUNTER_NR = 0

            TOTAL_TIME_WATCH.reset_time()
            if SYSTEM_ON == 1:
                TOTAL_TIME_WATCH.start()
            PRODUCTIVE_RUN_TIME_WATCH.reset_time()
            STOP_TIME_WATCH.reset_time()
            BOBIN_TIME_WATCH.reset_time()
            ARIZA_TIME_WATCH.reset_time()
            COZGU_TIME_WATCH.reset_time()
            AYAR_TIME_WATCH.reset_time()

            PRODUCTIVE_RUN_TIME = 0
            STOP_TIME = 0
            BOBIN_TIME = 0
            ARIZA_TIME = 0
            COZGU_TIME = 0
            AYAR_TIME = 0
            TOTAL_TIME = 0

            RESET_CHANGED = 1
            RESET_PUSHED = 0
            LOGGING.log_info('Counter reset')

        sleep(sleep_time)


def loop(sleep_time):
    """ Description """

    LOGGING.log_info('gpio_check loop begins.')
    while not is_shutdown:
        gpio_check()
        sleep(sleep_time)


def start_threading():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(event_counter, 0.1)
        executor.submit(event_reset, 0.5)
        executor.submit(loop, 0.2)
        executor.submit(lcd_refresh, 0.3)
        # executor.submit(json_refresh, 10)


# def add_events():
#     """ Description """
#     # BTN_START_STOP.add_callback(mode='both', callback=event_start_stop)
#     BTN_COUNTER.add_callback(mode='both', callback=event_counter)
#     # BTN_RESET.add_callback(mode='both', callback=event_reset)


if __name__ == '__main__':

    LOGGING.log_info('System loaded.')
    try:
        # add_events()
        start_threading()
        gpio_check_start_stop()
        # loop()

    except (KeyboardInterrupt, SystemExit):
        is_shutdown = True
        print('keyboard interrupt detected')
        LOGGING.log_info('System stopped.')
        classes.gpio_cleanup()
        LCD.lcd_close()
    # end of program
    # ##############
