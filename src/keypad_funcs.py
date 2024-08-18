# #######
# Imports
from time import sleep
from classes import keypad
from classes import lcd_module
from classes import os_commands
from classes import log_info
from classes import json_funcs
# from classes import os_commands

# #####
# Setup
CONFIG_JSON = json_funcs.get_setup()

LOGGING = log_info.LogInfo(CONFIG_JSON['main']['log'],
                          CONFIG_JSON['main']['log_level'],
                          CONFIG_JSON['main']['log_path'])

LCD = lcd_module.LcdModule()

KEYPAD_INSTALL = CONFIG_JSON['module']['keypad']['install']
if KEYPAD_INSTALL is True:
    KEY_PAD = keypad.KeyPad()

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
                # JSON_FUNCS.change_json(what='Given_Total_Counter', state=TOTAL_COUNTER)
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
                            # JSON_FUNCS.change_json(what='Given_Counter', state=COUNTER_NR)
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
