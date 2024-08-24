# -*- coding: utf-8 -*-
""" Description """

import json
from .time import get_date_time
from .log_info import LogInfo
from .mqtt import *
from os import path

def get_setup(setup_path="/home/pi/cesit_dijitallesme/setup.json"):
    """ Description """
    with open(setup_path, 'r') as file:
        config_json = json.load(file)
        return config_json


class JsonFuncs:
    """ Description """

    def __init__(self, setup_path="/home/pi/cesit_dijitallesme/setup.json"):

        mqtt_module = MQTTModule("device1")
        mqtt_module.connect()

        config_json = get_setup()
        self.logging = LogInfo(config_json['main']['log'],
                               config_json['main']['log_level'],
                               config_json['main']['log_path'])

        setup_json = get_setup(setup_path)
        self.device_name = setup_json['main']['device_name']
        self.mac_address = setup_json['main']['mac_address']
        self.path_current_json = setup_json['main']['path_current_json']
        self.path_cycle_json = setup_json['main']['path_cycle_json']

        data_js = {
            "device_name": self.device_name,
            "_id": self.device_name + "_current",
            "MAC-Adresi": self.mac_address,
            "Son Reset Tarihi": 0,
            "Döngü": 0,
            "Makine Durumu": "Kapalı",
            "Counter": 0,
            "Toplam düğüm sayısı": 0,
            "Kalan düğüm sayısı": 0,
            "Toplam çalışma süresi": 0,
            "Aktiv çalışma süresi": 0,
            "Bobin süresi": 0,
            "Arıza süresi": 0,
            "Çözgü süresi": 0,
            "Ayar süresi": 0, "Çalışma hızı": 0,
            "Tahmini kalan süre": 0,
            "Verim": 0
        }
        expected_keys = set(data_js.keys())

        # Überprüfen, ob die Datei existiert
        if path.exists('data.json'):
            # Versuche, die Datei zu öffnen und zu lesen
            with open('data.json', 'r') as file:
                data = json.load(file)
            json_keys = set(data.keys())
            
            # Wenn die Schlüssel nicht übereinstimmen, data_js verwenden
            if json_keys != expected_keys:
                data = data_js
        else:
            # Wenn die Datei nicht existiert, data_js verwenden
            data = data_js

        # TODO: hier muss json struktur angepasst werden. Ich brauche data.json from target.
        data_js['Counter'] = data['Counter']
        self.time_btw_counter = None
        self.total_counter = data['Toplam düğüm sayısı']

        try:
            # all device_name = current + cycles, that's why -1
            # TODO: get last cycle
            self.cycle = data['Döngü']
        except Exception as e:
            self.cycle = 0
            self.logging.log_info(e)
            self.logging.log_info('No Cycle exits. Creating new _id=0')

        try:
            self.total_time = data['Toplam çalışma süresi']
            self.total_time = float(self.total_time)
        except Exception as e:
            self.total_time = 0
            self.logging.log_info(e)

            self.logging.log_info('decelerated total_time = 0')

        self.remainder_time = None

        try:
            self.productive_run_time = data['Aktiv çalışma süresi']
            self.productive_run_time = float(self.productive_run_time)
        except Exception as e:
            self.productive_run_time = 0
            self.logging.log_info(e)

            self.logging.log_info('decelerated productive run_time = 0')

        self.remainder_time = None

        try:
            self.stop_time = data[ 'Durma süresi']
            self.stop_time = float(self.stop_time)
        except Exception as e:
            self.stop_time = 0
            self.logging.log_info(e)

            self.logging.log_info('decelerated stop_time = 0')

        try:
            self.bobin_time = data['Bobin süresi']
            self.bobin_time = float(self.bobin_time)
        except Exception as e:
            self.bobin_time = 0
            self.logging.log_info(e)

            self.logging.log_info('decelerated bobin_time = 0')

        try:
            self.ariza_time = ['Arıza süresi']
            self.ariza_time = float(self.ariza_time)
        except Exception as e:
            self.ariza_time = 0
            self.logging.log_info(e)

            self.logging.log_info('decelerated ariza_time = 0')

        try:
            self.cozgu_time = data['Çözgü süresi']
            self.cozgu_time = float(self.cozgu_time)
        except Exception as e:
            self.cozgu_time = 0
            self.logging.log_info(e)

            self.logging.log_info('decelerated cozgu_time = 0')

        try:
            self.ayar_time = data['Ayar süresi']
            self.ayar_time = float(self.ayar_time)
        except Exception as e:
            self.ayar_time = 0
            self.logging.log_info(e)

            self.logging.log_info('decelerated ayar_time = 0')

        try:
            self.total_time = data['Toplam çalışma süresi']
            self.total_time = float(self.total_time)
        except Exception as e:
            self.total_time = 0
            self.logging.log_info(e)

            self.logging.log_info('decelerated total_time = 0')

        try:
            self.productivity = data['Verim']
            self.productivity = float(self.productivity)
        except Exception as e:
            self.productivity = 0
            self.logging.log_info(e)

            self.logging.log_info('decelerated total_time = 0')

        try:
            self.reset_time = data['Son Reset Tarihi']
            self.reset_time = float(self.reset_time)
        except Exception as e:
            self.reset_time = 0
            self.logging.log_info(e)

    def get_counter(self):
        """ Description """
        return self.counter_nr

    def get_total_counter(self):
        """ Description """
        return self.total_counter

    def get_saved_total_time(self):
        return self.total_time

    def get_saved_productive_run_time(self):
        return self.productive_run_time

    def get_saved_stop_time(self):
        return self.stop_time

    def get_saved_bobin_time(self):
        return self.bobin_time

    def get_saved_ariza_time(self):
        return self.ariza_time

    def get_saved_cozgu_time(self):
        return self.cozgu_time

    def get_saved_ayar_time(self):
        return self.ayar_time

    # TODO: Makine Durumu": "Kapalı" vielleicht muss auch letzte State geschrieben werden.
    def __export_json(self):
        data_js = {
            "device_name": self.device_name,
            "_id": self.device_name + "_current",
            "MAC-Adresi": self.mac_address,
            "Son Reset Tarihi": self.reset_time,
            "Döngü": self.cycle,
            "Makine Durumu": "Kapalı",
            "Counter": self.counter_nr,
            "Toplam düğüm sayısı": self.total_counter,
            "Kalan düğüm sayısı": self.total_counter - self.counter_nr,
            "Toplam çalışma süresi": self.total_time,
            "Aktiv çalışma süresi": self.productive_run_time,
            "Bobin süresi": self.bobin_time,
            "Arıza süresi": self.ariza_time,
            "Çözgü süresi": self.cozgu_time,
            "Ayar süresi": self.ayar_time,
            "Çalışma hızı": self.time_btw_counter,
            "Tahmini kalan süre": self.remainder_time,
            "Verim": self.productivity
        }

        with open(self.path_current_json, 'w') as json_file:
            json.dump(data_js, json_file)

    # def __export_cycle(self):
    #     cursor = self.mycol.find({"_id": self.device_name + "_cycle_"})
    #     data_js = list(cursor)

    #     with open(self.path_current_json, 'w') as json_file:
    #         json.dump(data_js, json_file)

    # def __write_cycle(self):
    #     write_id = {
    #         "device_name": self.device_name,
    #         "_id": self.device_name + "_cycle_" + str(self.cycle),
    #         "Reset Tarihi": self.reset_time,
    #         "Tamamlanan Counter": self.counter_nr,
    #         "Toplam düğüm sayısı": self.total_counter,
    #         "Kalan düğüm sayısı": self.total_counter - self.counter_nr,
    #         "Toplam çalışma süresi": self.total_time,
    #         "Aktiv çalışma süresi": self.productive_run_time,
    #         "Durma süresi": self.stop_time,
    #         "Bobin süresi": self.bobin_time,
    #         "Arıza süresi": self.ariza_time,
    #         "Çözgü süresi": self.cozgu_time,
    #         "Ayar süresi": self.ayar_time,
    #         "Çalışma hızı": self.time_btw_counter,
    #         "Verim": self.productivity
    #     }
    #     self.mycol.insert_one(write_id)

    def change_json(self, what, state=None):
        """change_json"""

        if what == 'kapali':
            self.data['Makine Durumu'] = 'Kapalı'

        elif what == 'start':
            self.data['Makine Durumu'] = 'Çalışıyor'

        elif what == 'stop':
            self.data['Makine Durumu'] =  'Duruyor'

        elif what == 'counter':
            self.counter_nr = state[0]
            self.data['Counter'] = state[0]

            remainder_counter = self.total_counter - state[0]
            if remainder_counter >= 0:
                self.data['Kalan düğüm sayısı'] = remainder_counter
            else:
                self.data['Kalan düğüm sayısı'] = 0
            try:
                # Speed: counter time between counters
                self.time_btw_counter = round(state[2], 3)
            except ZeroDivisionError as e:
                self.time_btw_counter = 0
                self.logging.log_info('speed: ' + str(e))

            self.productive_run_time = state[1]
            self.data['Aktiv çalışma süresi'] = self.productive_run_time
            self.data['Çalışma hızı'] = self.time_btw_counter

            try:
                self.remainder_time = round(remainder_counter * self.time_btw_counter, 2)
                if self.remainder_time < 0:
                    self.remainder_time = 0
            except ZeroDivisionError as e:
                self.remainder_time = 0
                self.logging.log_info('remainder_time: ' + str(e))

            self.data['Tahmini kalan süre'] = self.remainder_time

            self.total_time = state[3]
            self.data['Toplam çalışma süresi'] = state[3]

        elif what == 'reset':
            self.reset_time = get_date_time()
            self.data['Son Reset Tarihi'] = self.reset_time

            # self.__write_cycle()
            # self.cycle = self.cycle + 1
            # self.mycol.update_one({"_id": self.device_name + "_current"},
            #                       {"$set": {'Döngü': self.cycle}})

        elif what == 'bobin':
            self.data['Makine Durumu'] = 'Duruyor - Bobin değişimi'

        elif what == 'cozgu':
            self.data['Makine Durumu'] = 'Duruyor - Çözgü'

        elif what == 'ariza':
            self.data['Makine Durumu'] = 'Duruyor - Arıza'

        elif what == 'ayar':
            self.data['Makine Durumu'] = 'Duruyor - Ayar'

        elif what == 'Given_Total_Counter':
            self.total_counter = state
            self.data['Toplam düğüm sayısı'] = state

        elif what == 'Given_Counter':
            self.counter_nr = state
            self.data['Counter'] = state

        elif what == 'write_status_times':
            self.productive_run_time = state[0]
            self.stop_time = state[1]
            self.bobin_time = state[2]
            self.ariza_time = state[3]
            self.cozgu_time = state[4]
            self.ayar_time = state[5]
            self.total_time = state[6]

            try:
                self.productivity = round(self.productive_run_time / self.total_time, 2)
            except ZeroDivisionError as e:
                self.productivity = 0
                self.logging.log_info('productivity: ' + str(e))

            self.data['Aktiv çalışma süresi'] = self.productive_run_time
            self.data['Durma süresi'] = self.stop_time
            self.data['Bobin süresi'] = self.bobin_time
            self.data['Arıza süresi'] = self.ariza_time
            self.data['Çözgü süresi'] = self.cozgu_time
            self.data['Ayar süresi'] = self.ayar_time
            self.data['Toplam çalışma süresi'] = self.total_time            
            self.data['Verim'] = self.productivity

        # Export as Jsonfile for Monitor
        self.__export_json()
