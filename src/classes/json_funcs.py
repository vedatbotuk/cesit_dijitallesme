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

        self.setup_json = get_setup(setup_path)
        self.device_name = self.setup_json['main']['device_name']
        self.path_json = self.setup_json['main']['path_json']
        self.path_database = self.setup_json['main']['path_database']

        #################
        # tinydb database
        if path_exists.isfile(self.path_database):
            self.db = TinyDB(self.path_database)
            self.logging.log_info('Tiny-Database exists')
            self.logging.log_info('Tiny-Database loaded from ' + self.path_database)
        else:
            self.db = TinyDB(self.path_database)
            self.db.insert({
                "id": self.device_name,
                "Makine Durumu": "Kapalı",
                "Counter": 0,
                "Son Reset Tarihi": "",
                "Toplam düğüm sayısı": 0,
                "Kalan düğüm sayısı": 0,
                "Çalışma süresi": "",
                "Çalışma hızı": "",
                "Tahmini kalan süre": ""
            })
            self.logging.log_info('Tiny-Database creating')
        # ###############

        self.counter_nr = int(self.db.all()[0]['Counter'])
        self.speed = None
        self.total_counter = int(self.db.all()[0]['Toplam düğüm sayısı'])

        try:
            self.run_time = float(self.db.all()[0]['Çalışma süresi'].split(' ', 1)[0]) * 3600
        except Exception as e:
            self.run_time = 0
            self.logging.log_info(e)
            self.logging.log_info('decelerated run_time = 0')

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
            self.db.update({'Makine Durumu': 'Kapalı'}, doc_ids=[1])

        elif what == 'start':
            self.db.update({'Makine Durumu': 'Çalışıyor'}, doc_ids=[1])

        elif what == 'stop':
            self.db.update({'Makine Durumu': 'Duruyor'}, doc_ids=[1])

        elif what == 'counter':
            self.db.update({'Counter': state[0]}, doc_ids=[1])

            remainder_counter = self.total_counter - state[0]
            if remainder_counter >= 0:
                self.db.update({'Kalan düğüm sayısı': remainder_counter}, doc_ids=[1])
            else:
                self.db.update({'Kalan düğüm sayısı': 0}, doc_ids=[1])

            try:
                self.speed = round(state[0] / state[1] * 60, 1)
            except ZeroDivisionError as e:
                self.speed = 0
                self.logging.log_info(e)

            self.run_time = round(state[1] / 3600, 2)
            self.db.update({'Çalışma süresi': str(self.run_time) + ' Saat'}, doc_ids=[1])

            if 0 < self.speed < 40:
                self.db.update({'Çalışma hızı': str(self.speed) + ' düğüm/dakkika'}, doc_ids=[1])

                self.remainder_time = round((self.total_counter / self.speed) / 60, 2)
                self.db.update({'Tahmini kalan süre': str(self.remainder_time) + ' Saat'}, doc_ids=[1])
            else:
                self.db.update({'Çalışma hızı': 'hesaplanıyor...'}, doc_ids=[1])
                self.db.update({'Tahmini kalan süre': 'hesaplanıyor...'}, doc_ids=[1])

        elif what == 'reset':
            self.system_time = self.time_obj.get_date_time()
            self.db.update({'Son Reset Tarihi': self.system_time}, doc_ids=[1])

        elif what == 'bobin':
            self.db.update({'Makine Durumu': 'Duruyor - Bobin değişimi'}, doc_ids=[1])

        elif what == 'cozgu':
            self.db.update({'Makine Durumu': 'Duruyor - Çözgü'}, doc_ids=[1])

        elif what == 'ariza':
            self.db.update({'Makine Durumu': 'Duruyor - Arıza'}, doc_ids=[1])

        elif what == 'ayar':
            self.db.update({'Makine Durumu': 'Duruyor - Ayar'}, doc_ids=[1])

        elif what == 'Given_Counter':
            self.total_counter = state

            self.db.update({'Kalan düğüm sayısı': state}, doc_ids=[1])
            self.db.update({'Toplam düğüm sayısı': state}, doc_ids=[1])

