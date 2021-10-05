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
            self.table = self.db.table('main')
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
            self.table = self.db.table('main')
            self.table.insert(db_js)
            self.logging.log_info('Tiny-Database creating')

        # self.db_backup = ''
        # ###############

        self.counter_nr = int(self.table.all()[0]['Counter'])

        self.speed = None
        self.total_counter = int(self.table.all()[0]['Toplam düğüm sayısı'])

        try:
            self.run_time = float(self.table.all()[0]['Çalışma süresi'].split(' ', 1)[0]) * 3600
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
            self.table.update({'Makine Durumu': 'Kapalı'}, doc_ids=[1])

        elif what == 'start':
            self.table.update({'Makine Durumu': 'Çalışıyor'}, doc_ids=[1])

        elif what == 'stop':
            self.table.update({'Makine Durumu': 'Duruyor'}, doc_ids=[1])

        elif what == 'counter':
            self.table.update({'Counter': state[0]}, doc_ids=[1])

            remainder_counter = self.total_counter - state[0]
            if remainder_counter >= 0:
                self.table.update({'Kalan düğüm sayısı': remainder_counter}, doc_ids=[1])
            else:
                self.table.update({'Kalan düğüm sayısı': 0}, doc_ids=[1])

            try:
                self.speed = round(state[0] / state[1] * 60, 1)
            except ZeroDivisionError as e:
                self.speed = 0
                self.logging.log_info(e)

            self.run_time = round(state[1] / 3600, 2)
            self.table.update({'Çalışma süresi': str(self.run_time) + ' Saat'}, doc_ids=[1])

            if 0 < self.speed < 40:
                self.table.update({'Çalışma hızı': str(self.speed) + ' düğüm/dakkika'}, doc_ids=[1])

                self.remainder_time = round((self.total_counter / self.speed) / 60, 2)
                self.table.update({'Tahmini kalan süre': str(self.remainder_time) + ' Saat'}, doc_ids=[1])
            else:
                self.table.update({'Çalışma hızı': 'hesaplanıyor...'}, doc_ids=[1])
                self.table.update({'Tahmini kalan süre': 'hesaplanıyor...'}, doc_ids=[1])

        elif what == 'reset':
            self.system_time = self.time_obj.get_date_time()
            self.table.update({'Son Reset Tarihi': self.system_time}, doc_ids=[1])

        elif what == 'bobin':
            self.table.update({'Makine Durumu': 'Duruyor - Bobin değişimi'}, doc_ids=[1])

        elif what == 'cozgu':
            self.table.update({'Makine Durumu': 'Duruyor - Çözgü'}, doc_ids=[1])

        elif what == 'ariza':
            self.table.update({'Makine Durumu': 'Duruyor - Arıza'}, doc_ids=[1])

        elif what == 'ayar':
            self.table.update({'Makine Durumu': 'Duruyor - Ayar'}, doc_ids=[1])

        elif what == 'Given_Counter':
            self.total_counter = state

            self.table.update({'Kalan düğüm sayısı': state}, doc_ids=[1])
            self.table.update({'Toplam düğüm sayısı': state}, doc_ids=[1])

    # def create_from_backup(self):
    #     self.db = TinyDB(self.db_backup)
    #
    # def create_backup(self, what):
    #     pass
