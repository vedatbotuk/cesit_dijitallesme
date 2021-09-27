#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """
import logging


class LogInfo:
    """ Description """
    def __init__(self, log_on_off, log_level, log_path):

        self.log_on_off = log_on_off
        self.log_path = log_path
        self.log_level = log_level

        self.logging_level = self.log_level

        if self.log_on_off == "on":
            if self.log_level == "info":
                self.logging_level = logging.INFO
            elif self.log_level == "debug":
                self.logging_level = logging.DEBUG

            # import logging
            logging.basicConfig(level=self.logging_level,
                                format="%(asctime)s %(levelname)-8s %(message)s",
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename=self.log_path,
                                )

    def log_info(self, text):
        """ Description """
        if (self.log_on_off == "on") and (self.log_level == "info"):
            logging.info(text)
        elif (self.log_on_off == "on") and (self.log_level == "debug"):
            logging.debug(text)
        else:
            pass
