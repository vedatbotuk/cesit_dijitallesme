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
        logging = LogInfo(config_json['main']['log'],
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
            logging.log_info('Database exists')
            logging.log_info('Database loaded from ' + self.path_json)
        else:
            self.data_js = {
                self.device_name: {
                    "Makine Durumu": "Çalışıyor",
                    "Counter": 0,
                    "Son Reset Tarihi": "-",
                    "Düğüm göz büyüklüğü": "-",
                    "Toplam düğüm sayısı": 30000,
                    "Kalan düğüm sayısı": "",
                    "Çalışma süresi": "-",
                    "Çalışma hızı": "-",
                    "Tahmini kalan süre": "-"
                }
            }
            logging.log_info('Created database with default_json')

            with open(self.path_json, 'w') as json_file:
                json.dump(self.data_js, json_file)

        self.counter_nr = int(self.data_js[self.device_name]['Counter'])
        # self.toplam_dugum = int(self.data_js[self.device_name]['Toplam düğüm sayısı'])

        self.time_obj = Time()
        self.system_time = self.time_obj.get_date_time()

    def get_counter(self):
        """ Description """
        return self.counter_nr

    def change_json(self, what, state=None):
        """change_json"""

        if what == 'kapali':
            self.data_js[self.device_name]['Makine Durumu'] = 'Kapalı'

        elif what == 'start':
            self.data_js[self.device_name]['Makine Durumu'] = 'Çalışıyor'

        elif what == 'stop':
            self.data_js[self.device_name]['Makine Durumu'] = 'Duruyor'

        elif what == 'counter':
            self.data_js[self.device_name]['Counter'] = state[0]
            # self.data_js[self.device_name]['Kalan düğüm sayısı'] = self.toplam_dugum - state[0]
            # self.data_js[self.device_name]['Çalışma hızı'] = str(state[0] / state[1]*60) + 'düğüm/dakkika'

        elif what == 'reset':
            self.system_time = self.time_obj.get_date_time()
            self.data_js[self.device_name]['Son Reset Tarihi'] = self.system_time

        elif what == 'bobin':
            self.data_js[self.device_name]['Makine Durumu'] = 'Duruyor - Bobin değişimi'

        elif what == 'cozgu':
            self.data_js[self.device_name]['Makine Durumu'] = 'Duruyor - Çözgü'

        elif what == 'ariza':
            self.data_js[self.device_name]['Makine Durumu'] = 'Duruyor - Arıza'

        elif what == 'ayar':
            self.data_js[self.device_name]['Makine Durumu'] = 'Duruyor - Ayar'

        with open(self.path_json, 'w') as json_file:
            json.dump(self.data_js, json_file)
