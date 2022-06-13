# -*- coding: utf-8 -*-
""" Description """

# imports
from datetime import datetime


def get_date_time():
    """ Description """
    # self.date_time_obj = datetime.now()
    return datetime.timestamp(datetime.now())


def get_minute():
    """ Description """
    now = datetime.timestamp(datetime.now())
    unix_time = datetime.fromtimestamp(now)
    return unix_time.strftime("%M")


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


class StartStopWatch:
    """ Description """
    def __init__(self, saved_run_time=0):

        self.date_time_obj = datetime.now()
        self.start_time = self.__get_unix_time()
        self.stop_time = self.__get_unix_time()
        self.run_time = saved_run_time
        self.tmp_time = self.run_time
        self.counter_time_first = 0

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

    def get_calculated_total_time(self):
        """ Description """
        self.run_time = self.tmp_time + self.__get_unix_time() - self.start_time
        return round(self.run_time, 1)

    def reset_time(self):
        self.run_time = 0
        self.tmp_time = 0

    def get_counter_time(self):
        counter_time_second = self.__get_unix_time()
        counter_time_diff = counter_time_second - self.counter_time_first
        self.counter_time_first = counter_time_second

        return counter_time_diff
