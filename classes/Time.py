#!/usr/bin/python3
''' Description '''

from datetime import datetime

class Time(object):
    ''' Description '''
    def __init__(self):
        self.system_time = ''

    def sync(self):
        ''' Description '''

        self.date_time_obj = datetime.now()

        if self.system_time != self.date_time_obj.strftime("%H:%M"):
            self.system_time = self.date_time_obj.strftime("%H:%M")

        return self.system_time


    def get_date_time(self):
        ''' Description '''
        self.date_time_obj = datetime.now()

        return self.date_time_obj.strftime("%d-%b-%Y (%H:%M:%S)")
