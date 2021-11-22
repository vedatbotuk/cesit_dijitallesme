#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

import json
from .time import Time
from .log_info import LogInfo
import pymongo


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

        setup_json = get_setup(setup_path)
        self.device_name = setup_json['main']['device_name']
        self.path_json = setup_json['main']['path_json']
        data_js = {
            "_id": self.device_name,
            "Makine Durumu": "Kapalı",
            "Counter": 0,
            "Son Reset Tarihi": "",
            "Toplam düğüm sayısı": 0,
            "Kalan düğüm sayısı": 0,
            "Çalışma süresi": 0,
            "Çalışma hızı": 0,
            "Tahmini kalan süre": 0
        }

        #################
        # mongodb database
        database_name = 'cesit_mensucat'
        collection_name = 'cesit_dijitallesme'

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient.database_names()
        if database_name in mydb:
            mydb = myclient[database_name]
            self.logging.log_info("The database exists.")
            collist = mydb.collection_names()
            if collection_name in collist:
                self.mycol = mydb[collection_name]
                self.logging.log_info("The collection exists.")
            else:
                self.mycol = mydb[collection_name]
                self.logging.log_info("Creating collection.")

        else:
            mydb = myclient[database_name]
            self.mycol = mydb[collection_name]
            self.logging.log_info("Creating database.")
            self.logging.log_info("Creating collection.")

        if not self.mycol.find({"_id": self.device_name}).count() > 0:
            self.mycol.insert_one(data_js)
            self.logging.log_info("Data does not exists, inserting default data.")
        # ###############

        self.counter_nr = self.mycol.find_one({"_id": self.device_name})['Counter']
        self.speed = None
        self.total_counter = self.mycol.find_one({"_id": self.device_name})['Toplam düğüm sayısı']

        try:
            self.run_time = self.mycol.find_one({"_id": self.device_name})['Çalışma süresi']
            self.run_time = float(self.run_time)
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

    def __export_json(self):
        cursor = self.mycol.find({"_id": self.device_name})
        data_js = list(cursor)

        with open(self.path_json, 'w') as json_file:
            json.dump(data_js, json_file)

    def change_json(self, what, state=None):
        """change_json"""

        if what == 'kapali':
            # self.db.update({'Makine Durumu': 'Kapalı'}, doc_ids=[1])
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Makine Durumu': 'Kapalı'}})

        elif what == 'start':
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Makine Durumu': 'Çalışıyor'}})

        elif what == 'stop':
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Makine Durumu': 'Duruyor'}})

        elif what == 'counter':
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Counter': state[0]}})

            remainder_counter = self.total_counter - state[0]
            if remainder_counter >= 0:
                self.mycol.update_one({"_id": self.device_name}, {"$set": {'Kalan düğüm sayısı': remainder_counter}})
            else:
                self.mycol.update_one({"_id": self.device_name}, {"$set": {'Kalan düğüm sayısı': 0}})

            try:
                self.speed = round(state[0] / state[1], 1)
            except ZeroDivisionError as e:
                self.speed = 0
                self.logging.log_info('speed: ' + str(e))

            self.run_time = state[1]
            self.mycol.update_one({"_id": self.device_name},
                                  {"$set": {'Çalışma süresi': self.run_time}})

            # if 0 < self.speed < 40:
            self.mycol.update_one({"_id": self.device_name},
                                  {"$set": {'Çalışma hızı': self.speed}})

            try:
                self.remainder_time = round((self.total_counter / self.speed) - self.run_time, 2)
                if self.remainder_time < 0:
                    self.remainder_time = 0
            except ZeroDivisionError as e:
                self.remainder_time = 0
                self.logging.log_info('remainder_time: ' + str(e))

            self.mycol.update_one({"_id": self.device_name},
                                  {"$set": {
                                      'Tahmini kalan süre': self.remainder_time}})

            # elif self.speed <= 0:
            #     self.mycol.update_one({"_id": self.device_name}, {"$set": {'Çalışma hızı': '...'}})
            #     self.mycol.update_one({"_id": self.device_name}, {"$set": {'Tahmini kalan süre': '...'}})

            # else:
            #     self.mycol.update_one({"_id": self.device_name}, {"$set": {'Çalışma hızı': 'hesaplanıyor...'}})
            #     self.mycol.update_one({"_id": self.device_name}, {"$set": {'Tahmini kalan süre': 'hesaplanıyor...'}})

        elif what == 'reset':
            self.system_time = self.time_obj.get_date_time()
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Son Reset Tarihi': self.system_time}})

        elif what == 'bobin':
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Makine Durumu': 'Duruyor - Bobin değişimi'}})

        elif what == 'cozgu':
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Makine Durumu': 'Duruyor - Çözgü'}})

        elif what == 'ariza':
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Makine Durumu': 'Duruyor - Arıza'}})

        elif what == 'ayar':
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Makine Durumu': 'Duruyor - Ayar'}})

        elif what == 'Given_Counter':
            self.total_counter = state

            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Kalan düğüm sayısı': state}})
            self.mycol.update_one({"_id": self.device_name}, {"$set": {'Toplam düğüm sayısı': state}})

        # Export as Jsonfile for Monitor
        self.__export_json()
