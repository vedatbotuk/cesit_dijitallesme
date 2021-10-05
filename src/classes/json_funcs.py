#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

import json
from os import path as path_exists
from .time import Time
from .log_info import LogInfo
from tinydb import TinyDB


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

        # self.data_js = {}
        self.setup_json = get_setup(setup_path)
        self.device_name = self.setup_json['main']['device_name']
        self.path_json = self.setup_json['main']['path_json']
        self.path_database = self.setup_json['main']['path_database']

        # tinydb database
        if path_exists.isfile(self.path_database):
            self.db = TinyDB(self.path_database)
            self.logging.log_info('Tiny-Database exists')
            self.logging.log_info('Tiny-Database loaded from ' + self.path_database)
        else:
            db_js = {
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
            self.db = TinyDB(self.path_database)
            self.db.insert(db_js)
            self.logging.log_info('Tiny-Database creating')

        # self.db_backup = ''
        # ###############

        self.counter_nr = int(self.db.all()[0]['Counter'])

        self.speed = None
        self.total_counter = int(self.db.all()[0]['Toplam düğüm sayısı'])

        try:
            self.run_time = float(self.db.all()[0]['Çalışma süresi'].split(' ', 1)[0]) * 3600
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
            self.db.update({'Makine Durumu' : 'Kapalı'})

        elif what == 'start':
            self.db.update({'Makine Durumu': 'Çalışıyor'})

        elif what == 'stop':
            self.db.update({'Makine Durumu': 'Duruyor'})

        elif what == 'counter':
            self.db.update({'Counter': state[0]})

            remainder_counter = self.total_counter - state[0]
            if remainder_counter >= 0:
                self.db.update({'Kalan düğüm sayısı': remainder_counter})
            else:
                self.db.update({'Kalan düğüm sayısı': 0})

            self.speed = round(state[0] / state[1] * 60, 1)

            self.run_time = round(state[1] / 3600, 2)
            self.db.update({'Çalışma süresi': str(self.run_time) + ' Saat'})

            if 0 < self.speed < 40:
                self.db.update({'Çalışma hızı': str(self.speed) + ' düğüm/dakkika'})

                self.remainder_time = round((self.total_counter / self.speed) / 60, 2)
                self.db.update({'Tahmini kalan süre': str(self.remainder_time) + ' Saat'})
            else:
                self.db.update({'Çalışma hızı': 'hesaplanıyor...'})
                self.db.update({'Tahmini kalan süre': 'hesaplanıyor...'})

        elif what == 'reset':
            self.system_time = self.time_obj.get_date_time()
            self.db.update({'Son Reset Tarihi': self.system_time})

        elif what == 'bobin':
            self.db.update({'Makine Durumu': 'Duruyor - Bobin değişimi'})

        elif what == 'cozgu':
            self.db.update({'Makine Durumu': 'Duruyor - Çözgü'})

        elif what == 'ariza':
            self.db.update({'Makine Durumu': 'Duruyor - Arıza'})

        elif what == 'ayar':
            self.db.update({'Makine Durumu': 'Duruyor - Ayar'})

        elif what == 'Given_Counter':
            self.total_counter = state

            self.db.update({'Kalan düğüm sayısı': state})
            self.db.update({'Toplam düğüm sayısı': state})

    # def create_from_backup(self):
    #     self.db = TinyDB(self.db_backup)
    #
    # def create_backup(self, what):
    #     pass
