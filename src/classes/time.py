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
    def __init__(self, saved_run_time=None):

        self.date_time_obj = datetime.now()
        self.start_time = self.__get_unix_time()
        self.stop_time = self.__get_unix_time()
        self.run_time = saved_run_time
        self.tmp_time = self.run_time

    def __get_unix_time(self):
        """ Description """
        self.date_time_obj = datetime.now()

        return datetime.timestamp(self.date_time_obj)

    def start(self):
        """ Description """
        self.start_time = self.__get_unix_time()

    def stop(self):
        """ Description """
        self.tmp_time = self.run_time

    def get_run_time(self):
        """ Description """
        self.run_time = self.tmp_time + self.__get_unix_time() - self.start_time
        return round(self.run_time, 1)

    def reset_time(self):
        self.run_time = 0
        self.tmp_time = 0
