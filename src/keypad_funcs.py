# #######
# Imports
import main


def given_counter():
    """ Description """
    return_number = None
    given_number = ''

    main.LCD.refresh_lcd('Given_Counter', given_number)

    while True:
        get_button = str(main.KEY_PAD.check_button())
        if get_button == 'C':
            break

        elif get_button == 'D':
            given_number = given_number[:-1]
            main.LCD.refresh_lcd('Given_Counter', given_number)

        elif get_button == '*':
            try:
                return_number = int(given_number)

                main.LCD.refresh_lcd('successfully', given_number)
                main.sleep(2)
                break

            except Exception as e:
                main.LCD.refresh_lcd('Counter_not_allowed')
                main.sleep(2)
                main.LCD.refresh_lcd('Given_Counter', given_number)
                return_number = None
                main.LOGGING.log_info(e)

        elif get_button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            given_number = given_number + get_button
            main.LCD.refresh_lcd('Given_Counter', given_number)

        main.sleep(0.2)

    return return_number


def keypad_give_total_counter():
    """ Description """
    global TOTAL_COUNTER, COUNTER_NR

    if main.KEYPAD_INSTALL is True:
        wait = 15
        checked = 0
        for cnt in range(0, wait):
            button_to_give_counter = main.KEY_PAD.check_button()
            if button_to_give_counter == "#":
                checked = checked + 1
            else:
                break
            main.sleep(0.2)

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

    if main.KEYPAD_INSTALL is True:
        wait = 15
        checked = 0
        for cnt in range(0, wait):
            button_to_give_total = main.KEY_PAD.check_button()
            if button_to_give_total == "D":
                checked = checked + 1
            else:
                break
            main.sleep(0.2)

        if checked == wait:
            given_code = ''
            main.LCD.refresh_lcd('Given_Code', given_code)

            while True:
                get_button = str(main.KEY_PAD.check_button())
                if get_button == 'C':
                    break

                elif get_button == 'D':
                    given_code = given_code[:-1]
                    main.LCD.refresh_lcd('Given_Code', given_code)

                elif get_button == '*':

                    if given_code == '100':
                        main.classes.os_commands.shutdown_system()
                        main.LCD.lcd_close()
                        exit()
                        break

                    elif given_code == '101':
                        main.classes.os_commands.reboot_system()
                        main.LCD.lcd_close()
                        exit()
                        break

                    elif given_code == '102':
                        main.classes.os_commands.restart_program()
                        main.LCD.lcd_close()
                        exit()
                        break

                    elif given_code == '103':
                        main.classes.os_commands.update_code()
                        main.LCD.lcd_close()
                        break

                    elif given_code == '104':
                        change_counter = given_counter()
                        if change_counter is not None:
                            COUNTER_NR = change_counter
                            # JSON_FUNCS.change_json(what='Given_Counter', state=COUNTER_NR)
                        break

                    else:
                        main.LCD.refresh_lcd('Code_not_exists')
                        main.sleep(2)
                        given_code = ''
                        main.LCD.refresh_lcd('Given_Code', given_code)

                elif get_button in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    given_code = given_code + get_button
                    main.LCD.refresh_lcd('Given_Code', given_code)

                main.sleep(0.2)


def show_total_counter():
    """ Description """
    global TOTAL_COUNTER, COUNTER_NR

    if main.KEYPAD_INSTALL is True:
        while True:
            button_to_give_total = main.KEY_PAD.check_button()
            if button_to_give_total == 'A':
                main.LCD.refresh_lcd(what='show_total', state=TOTAL_COUNTER)
            else:
                break
            main.sleep(0.5)


def show_remainder_counter():
    """ Description """
    global TOTAL_COUNTER, COUNTER_NR

    if main.KEYPAD_INSTALL is True:
        while True:
            button_to_give_remainder = main.KEY_PAD.check_button()
            if button_to_give_remainder == 'B':
                main.LCD.refresh_lcd(what='show_remainder', state=TOTAL_COUNTER - COUNTER_NR)
            else:
                break
            main.sleep(0.5)
