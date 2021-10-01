#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

import json
from os import path as path_exists
from .time import Time
from .log_info import LogInfo


def get_setup(setup_path="/home/pi/cesit_dijitallesme/setup.json"):
    """ Description """
    with open(setup_path, 'r') as file:
        config_json = json.load(file)
        return config_json


class JsonFuncs:
    """ Description """

    def __init__(self, setup_path="/home/pi/cesit_dijitallesme/setup.json"):

        config_json = get_setup()

        self.logging = LogInfo(config_json['main']['log'],
                               config_json['main']['log_level'],
                               config_json['main']['log_path'])

        self.data_js = {}
        self.setup_json = get_setup(setup_path)
        self.device_name = self.setup_json['main']['device_name']
        self.path_json = self.setup_json['main']['path_json']

        # create or get data_js
        # if not exists create file
        if path_exists.isfile(self.path_json):
            self.data_js = json.load(open(self.path_json, 'r'))
            self.logging.log_info('Database exists')
            self.logging.log_info('Database loaded from ' + self.path_json)
        else:
            self.data_js = {
                "id": self.device_name,
                "Makine Durumu": "Kapalı",
                "Counter": 0,
                "Son Reset Tarihi": "",
                "Toplam düğüm sayısı": 0,
                "Kalan düğüm sayısı": 0,
                "Çalışma süresi": "",
                "Çalışma hızı": "",
                "Tahmini kalan süre": ""
            }
            self.logging.log_info('Created database with default_json')
            try:
                with open(self.path_json, 'w') as json_file:
                    json.dump(self.data_js, json_file)
            except Exception as e:
                self.logging.log_info(e)

        self.counter_nr = int(self.data_js['Counter'])
        self.speed = None
        self.total_counter = int(self.data_js['Toplam düğüm sayısı'])

        try:
            self.run_time = float(self.data_js['Çalışma süresi'].split(' ', 1)[0]) * 3600
        except Exception as e:
            self.run_time = 0
            self.logging.log_info(e)

        self.remainder_time = None

        self.time_obj = Time()
        self.system_time = self.time_obj.get_date_time()

    def get_counter(self):
        """ Description """
        return self.counter_nr

    def get_total_counter(self):
        """ Description """
        return self.total_counter

    def get_saved_run_time(self):
        return self.run_time

    def change_json(self, what, state=None):
        """change_json"""

        if what == 'kapali':
            self.data_js['Makine Durumu'] = 'Kapalı'

        elif what == 'start':
            self.data_js['Makine Durumu'] = 'Çalışıyor'

        elif what == 'stop':
            self.data_js['Makine Durumu'] = 'Duruyor'

        elif what == 'counter':
            self.data_js['Counter'] = state[0]
            self.data_js['Kalan düğüm sayısı'] = self.total_counter - state[0]

            self.speed = round(state[0] / state[1] * 60, 1)

            if 0 < self.speed < 40:
                self.data_js['Çalışma hızı'] = str(self.speed) + ' düğüm/dakkika'

                self.run_time = round(state[1] / 3600, 2)
                self.data_js['Çalışma süresi'] = str(self.run_time) + ' Saat'

                self.remainder_time = round((self.total_counter / self.speed) / 60, 2)
                self.data_js['Tahmini kalan süre'] = str(self.remainder_time) + ' Saat'
            else:
                self.data_js['Çalışma hızı'] = 'hesaplanıyor...'
                self.data_js['Çalışma süresi'] = 'hesaplanıyor...'
                self.data_js['Tahmini kalan süre'] = 'hesaplanıyor...'

        elif what == 'reset':
            self.system_time = self.time_obj.get_date_time()
            self.data_js['Son Reset Tarihi'] = self.system_time

        elif what == 'bobin':
            self.data_js['Makine Durumu'] = 'Duruyor - Bobin değişimi'

        elif what == 'cozgu':
            self.data_js['Makine Durumu'] = 'Duruyor - Çözgü'

        elif what == 'ariza':
            self.data_js['Makine Durumu'] = 'Duruyor - Arıza'

        elif what == 'ayar':
            self.data_js['Makine Durumu'] = 'Duruyor - Ayar'

        elif what == 'Given_Counter':
            self.total_counter = state
            self.data_js['Kalan düğüm sayısı'] = state
            self.data_js['Toplam düğüm sayısı'] = state

        # if self.tmp_data_js != self.data_js:
        #     print(self.tmp_data_js)
        try:
            with open(self.path_json, 'w') as json_file:
                json.dump(self.data_js, json_file)
        except Exception as e:
            self.logging.log_info(e)
