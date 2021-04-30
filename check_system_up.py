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

        button_state_bobin = GPIO.input(btn_bobin)
        if button_state_bobin:
            write_lcd('bobin', None)
            change_json('bobin', None)
            bobin_state = 1
        else:
            write_lcd('stop', None)
            change_json('stop', None)
            bobin_state = 0

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