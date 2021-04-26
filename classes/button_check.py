#!/usr/bin/python3

from RPi import GPIO

class Device:
    def __init__(self, gpio, name_state=None, name_json=None, name_nr_status=None):
        self.name_state = name_state
        self.name_json = name_json
        self.name_nr_status = name_nr_status

        def check_btn(name_btn, name_state, name_json, name_nr_status):
            if name_btn == 1:
                if name_state == 0:
                    if (type(name_nr_status)) == int:
                        name_nr = name_nr_status + 1

                    change_json(name_json, name_nr_status)
                    name_state = 1
                    print(name_json + '= ' + name_nr_status)