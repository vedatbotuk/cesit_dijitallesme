# !/usr/bin/python3
""" Description """

# Imports
import json
import os
from time import sleep
import classes as classes

# Logging
# TODO logging

# Setup
with open('../setup.json', 'r') as f:
    config_json = json.load(f)

path_json = config_json['main']['path_json']
path_json_default = config_json['main']['path_json_default']

lcd = classes.LcdModule

time_obj = classes.Time()

system_time = ''
data_js = {}

# # btn_kapali = 4
# kapali_state = 0
#
# # btn_counter = 17
# counter_state = 0
#
# # btn_reset = 27
# reset_state = 0
counter_nr = 0
system_on = 0
machine_start_stop = 0
stop_options_array = []
#
# # btn_start_stop = 22
# start_stop_state = 0
#
# # btn_bobin = 5
# # bobin_state = 0
#
# # btn_cozgu = 6
# cozgu_state = 0
#
# # btn_ariza = 13
# ariza_state = 0
#
# # btn_ayar = 19
# ayar_state = 0

btn_kapali = classes.ButtonSwitch(config_json['buttons']['btn_kapali'])
btn_start_stop = classes.ButtonSwitch(config_json['buttons']['btn_start_stop'])
btn_cozgu = classes.ButtonSwitch(config_json['buttons']['btn_cozgu'])
btn_ariza = classes.ButtonSwitch(config_json['buttons']['btn_ariza'])
btn_ayar = classes.ButtonSwitch(config_json['buttons']['btn_ayar'])
btn_bobin = classes.ButtonSwitch(config_json['buttons']['btn_bobin'])


def setup():
    """Takes in a number n, returns the square of n"""
    global data_js, counter_nr, path_json

    # if not exists create file
    if os.path.isfile(path_json):
        data_js = json.load(open(path_json, 'r'))
        counter_nr = int(data_js['Devices']['Pilot']['Counter'])

    else:
        with open(path_json_default, 'r') as json_file:
            json.dump(data_js, json_file)


def change_json(what, state):
    """change_json"""
    if what == 'kapali':
        data_js['Devices']['Pilot']['Makine Durumu'] = 'Kapalı'

    elif what == 'start':
        data_js['Devices']['Pilot']['Makine Durumu'] = 'Çalışıyor'

    elif what == 'stop':
        data_js['Devices']['Pilot']['Makine Durumu'] = 'Duruyor'

    elif what == 'counter':
        data_js['Devices']['Pilot']['Counter'] = state

    elif what == 'reset':
        data_js['Devices']['Pilot']['Son Reset Tarihi'] = state

    elif what == 'bobin':
        data_js['Devices']['Pilot']['Makine Durumu'] = 'Duruyor - Bobin değişimi'

    elif what == 'cozgu':
        data_js['Devices']['Pilot']['Makine Durumu'] = 'Duruyor - Çözgü'

    elif what == 'ariza':
        data_js['Devices']['Pilot']['Makine Durumu'] = 'Duruyor - Arıza'

    elif what == 'ayar':
        data_js['Devices']['Pilot']['Makine Durumu'] = 'Duruyor - Ayar'

    with open(path_json, 'w') as json_file:
        json.dump(data_js, json_file)


def write_lcd(what, show):
    """ Description """
    global system_time

    if what == 'kapali':
        lcd.write_row1(system_time + '    ' + u'kapali')

    elif what == 'start':
        lcd.write_row1(system_time + ' ' + u'calisiyor')

    elif what == 'stop':
        lcd.write_row1(system_time + '   ' + u'duruyor')

    elif what == 'bobin':
        lcd.write_row1(system_time + '     ' + u'bobin')

    elif what == 'cozgu':
        lcd.write_row1(system_time + '     ' + u'cozgu')

    elif what == 'ariza':
        lcd.write_row1(system_time + '     ' + u'ariza')

    elif what == 'ayar':
        lcd.write_row1(system_time + '      ' + u'ayar')

    elif what == 'reset':
        lcd.write_row2(u'Counter= ' + '0      ')

    elif what == 'counter':
        lcd.write_row2(u'Counter= ' + str(show))


def gpio_options_check():
    global stop_options_array

    stop_options_array = []
    options_changed = 0

    # BOBIN SWITCH ##############
    # ###########################
    # ab hier testet alle nebenarbeiten an der maschine
    btn_bobin_checked = btn_bobin.check_switch()
    if btn_bobin_checked is False:
        stop_options_array.append('bobin')
        options_changed = 1
    elif btn_bobin_checked is True:
        stop_options_array.remove('bobin')
        options_changed = 1
    # BOBIN SWITCH --------------
    # ---------------------------

    # COZGU SWITCH ##############
    # ###########################
    btn_cozgu_checked = btn_cozgu.check_switch()
    if btn_cozgu_checked is False:
        stop_options_array.append('cozgu')
        options_changed = 1
    elif btn_cozgu_checked is True:
        stop_options_array.remove('ariza')
        options_changed = 1
    # COZGU SWITCH --------------
    # ---------------------------

    # ARIZA SWITCH ##############
    # ###########################
    btn_ariza_checked = btn_ariza.check_switch()
    if btn_ariza_checked is False:
        stop_options_array.append('ariza')
        options_changed = 1
    elif btn_ariza_checked is True:
        stop_options_array.remove('ariza')
        options_changed = 1
    # ARIZA SWITCH --------------
    # ---------------------------

    # AYAR SWITCH ###############
    # ###########################
    btn_ayar_checked = btn_ayar.check_switch()
    if btn_ayar_checked is False:
        stop_options_array.append('ayar')
        options_changed = 1
    elif btn_ayar_checked is True:
        stop_options_array.remove('ayar')
        options_changed = 1
    # AYAR SWITCH ---------------
    # ---------------------------

    if options_changed == 1 and len(stop_options_array) != 0:
        # last entry in array
        write_lcd(stop_options_array[len(stop_options_array) - 1], None)
        change_json(stop_options_array[len(stop_options_array) - 1], None)


def gpio_check1():
    """ Description """
    global system_on, machine_start_stop, counter_nr, btn_start_stop, btn_bobin, btn_cozgu, btn_ariza, btn_ayar, \
        btn_kapali, stop_options_array

    options_changed = 0

    # AC/KAPA SWITCH
    # ###########################
    btn_kapali_checked = btn_kapali.check_switch()
    if btn_kapali_checked is False:
        stop_options_array.append('kapali')
        system_on = 0
        options_changed = 1
    elif btn_kapali_checked is True:
        stop_options_array.remove('kapali')
        system_on = 1
    # AC/KAPA SWITCH ------------
    # ---------------------------

    if system_on == 1:
        # START/STOP SWITCH ##############
        # ################################
        # start stop und nebenarbeiten an der maschine
        # wenn start switch on, zeigt nur start bzw. calisiyor
        btn_start_stop_checked = btn_start_stop.check_switch()
        if btn_start_stop_checked is False:
            if 'stop' in stop_options_array: stop_options_array.remove('stop')
            stop_options_array.append('start')
            machine_start_stop = 1
            options_changed = 1
        # maschiene gestopt
        # zusatzlich kann signalisiert werden, warum die maschine gestopt
        elif btn_start_stop_checked is True:
            if 'start' in stop_options_array: stop_options_array.remove('start')
            stop_options_array.append('stop')
            machine_start_stop = 0
            options_changed = 1
        # START/STOP SWITCH --------
        # ---------------------------

    if machine_start_stop == 0 and system_on == 1:
        # BOBIN SWITCH ##############
        # ###########################
        # ab hier testet alle nebenarbeiten an der maschine
        btn_bobin_checked = btn_bobin.check_switch()
        if btn_bobin_checked is False:
            stop_options_array.append('bobin')
            options_changed = 1
        elif btn_bobin_checked is True:
            stop_options_array.remove('bobin')
            options_changed = 1
        # BOBIN SWITCH --------------
        # ---------------------------

        # COZGU SWITCH ##############
        # ###########################
        btn_cozgu_checked = btn_cozgu.check_switch()
        if btn_cozgu_checked is False:
            stop_options_array.append('cozgu')
            options_changed = 1
        elif btn_cozgu_checked is True:
            stop_options_array.remove('ariza')
            options_changed = 1
        # COZGU SWITCH --------------
        # ---------------------------

        # ARIZA SWITCH ##############
        # ###########################
        btn_ariza_checked = btn_ariza.check_switch()
        if btn_ariza_checked is False:
            stop_options_array.append('ariza')
            options_changed = 1
        elif btn_ariza_checked is True:
            stop_options_array.remove('ariza')
            options_changed = 1
        # ARIZA SWITCH --------------
        # ---------------------------

        # AYAR SWITCH ###############
        # ###########################
        btn_ayar_checked = btn_ayar.check_switch()
        if btn_ayar_checked is False:
            stop_options_array.append('ayar')
            options_changed = 1
        elif btn_ayar_checked is True:
            stop_options_array.remove('ayar')
            options_changed = 1
        # AYAR SWITCH ---------------
        # ---------------------------

    if options_changed == 1 and len(stop_options_array) != 0:
        # last entry in array
        write_lcd(stop_options_array[len(stop_options_array) - 1], None)
        change_json(stop_options_array[len(stop_options_array) - 1], None)


def gpio_check():
    """ Description """
    global system_on, machine_start_stop, counter_nr, btn_start_stop, btn_bobin, btn_cozgu, btn_ariza,\
        btn_ayar, btn_kapali

    # AC/KAPA SWITCH
    # ###########################
    btn_kapali_checked = btn_kapali.check_switch()
    if btn_kapali_checked is False:
        system_on = 0
        write_lcd('kapali', None)
        change_json('kapali', None)
        print('kapali')

    elif btn_kapali_checked is True:
        print('acik')
        system_on = 1
    # AC/KAPA SWITCH ------------
    # ---------------------------

    if system_on == 1:
        # START/STOP SWITCH ##############
        # ################################
        # start stop und nebenarbeiten an der maschine
        # wenn start switch on, zeigt nur start bzw. calisiyor
        btn_start_stop_checked = btn_start_stop.check_switch()
        if btn_start_stop_checked is False:
            machine_start_stop = 1
            write_lcd('start', None)
            change_json('start', None)
            print('start')
        # maschiene gestopt
        # zusatzlich kann signalisiert werden, warum die maschine gestopt
        elif btn_start_stop_checked is True:
            machine_start_stop = 0
            write_lcd('stop', None)
            change_json('stop', None)
            # print('stop')
        # START/STOP SWITCH --------
        # ---------------------------

    if machine_start_stop == 0 and system_on == 1:
        gpio_options_check()

    # if machine_start_stop == 0 and system_on == 1:
    #     # BOBIN SWITCH ##############
    #     # ###########################
    #     # ab hier testet alle nebenarbeiten an der maschine
    #     btn_bobin_checked = btn_bobin.check_switch()
    #     if btn_bobin_checked is False:
    #         write_lcd('bobin', None)
    #         change_json('bobin', None)
    #         # print('bobin')
    #     elif btn_bobin_checked is True:
    #         write_lcd('stop', None)
    #         change_json('stop', None)
    #         # print('duruyor')
    #     # BOBIN SWITCH --------------
    #     # ---------------------------
    #
    #     # COZGU SWITCH ##############
    #     # ###########################
    #     btn_cozgu_checked = btn_cozgu.check_switch()
    #     if btn_cozgu_checked is False:
    #         write_lcd('cozgu', None)
    #         change_json('cozgu', None)
    #         # print('cozgu')
    #     elif btn_cozgu_checked is True:
    #         write_lcd('stop', None)
    #         change_json('stop', None)
    #         # print('duruyor')
    #     # COZGU SWITCH --------------
    #     # ---------------------------
    #
    #     # ARIZA SWITCH ##############
    #     # ###########################
    #     btn_ariza_checked = btn_ariza.check_switch()
    #     if btn_ariza_checked is False:
    #         write_lcd('ariza', None)
    #         change_json('ariza', None)
    #         print('ariza')
    #     elif btn_ariza_checked is True:
    #         write_lcd('stop', None)
    #         change_json('stop', None)
    #         # print('duruyor')
    #     # ARIZA SWITCH --------------
    #     # ---------------------------
    #
    #     # AYAR SWITCH ###############
    #     # ###########################
    #     btn_ayar_checked = btn_ayar.check_switch()
    #     if btn_ayar_checked is False:
    #         write_lcd('ayar', None)
    #         change_json('ayar', None)
    #         # print('ayar')
    #     elif btn_ayar_checked is True:
    #         write_lcd('stop', None)
    #         change_json('stop', None)
    #         # print('duruyor')
    #     # AYAR SWITCH ---------------
    #     # ---------------------------


def loop():
    """ Description """
    global system_time

    while True:
        gpio_check()
        # test()
        system_time = time_obj.sync()
        sleep(0.2)


def write_lcd_json_counter(channel):
    global counter_nr

    if machine_start_stop == 1:
        counter_nr = counter_nr + 1
        write_lcd('counter', counter_nr)
        change_json('counter', counter_nr)


def write_lcd_json_btn_reset(channel):
    global counter_nr

    if machine_start_stop == 0:
        counter_nr = 0
        # print('Reset' + ":")
        write_lcd('reset', counter_nr)
        change_json('reset', time_obj.get_date_time())
        change_json('counter', 0)


classes.ButtonSwitch(config_json['buttons']['btn_counter'], callback=write_lcd_json_counter)
classes.ButtonSwitch(config_json['buttons']['btn_reset'], callback=write_lcd_json_btn_reset)

if __name__ == '__main__':
    setup()

    try:
        loop()
        classes.gpio_cleanup()

    except KeyboardInterrupt:
        print('keyboard interrupt detected')
        classes.gpio_cleanup()
    # endprogram()
