#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

# imports
from datetime import datetime


class Time:
    """ Description """
    def __init__(self):

        self.date_time_obj = ''
        self.system_time = ''

    def sync(self):
        """ Description """

        self.date_time_obj = datetime.now()

        if self.system_time != self.date_time_obj.strftime("%H:%M"):
            self.system_time = self.date_time_obj.strftime("%H:%M")

        return self.system_time

    def get_date_time(self):
        """ Description """
        self.date_time_obj = datetime.now()

        return self.date_time_obj.strftime("%d-%b-%Y (%H:%M:%S)")


class StartStopWatch:
    """ Description """
    def __init__(self):

        # TODO: get information from data.json

        self.date_time_obj = datetime.now()
        self.start_time = self.__get_unix_time()
        self.stop_time = self.__get_unix_time()
        self.total_time = 0
        self.tmp_time = 0

    def __get_unix_time(self):
        """ Description """
        self.date_time_obj = datetime.now()

        return datetime.timestamp(self.date_time_obj)

    def start(self):
        """ Description """
        # self.tmp_time = 0
        self.start_time = self.__get_unix_time()

    def stop(self):
        """ Description """
        # self.stop_time = self.__get_unix_time()
        # self.tmp_time = self.stop_time - self.start_time
        self.tmp_time = self.total_time

    def get_run_time(self):
        """ Description """
        # total_time = self.tmp_time + self.__get_unix_time() - self.start_time
        self.total_time = self.tmp_time + self.__get_unix_time() - self.start_time
        # print(int(total_time))
        return round(self.total_time, 1)

    def reset_time(self):
        self.total_time = 0
        self.tmp_time = 0