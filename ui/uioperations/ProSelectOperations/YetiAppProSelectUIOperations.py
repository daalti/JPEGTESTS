#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import time
import requests
import unicodedata
from dunetuf.ui.uioperations.BaseOperations.IYetiAppUIOperations import IYetiAppUIOperations
from dunetuf.localization.LocalizationHelper import LocalizationHelper


HeaderID = '#Version1Text'
SubHeaderMsgIDtxt = '#Version2Text'


class YetiAppProSelectUIOperations(IYetiAppUIOperations):

    def __init__(self, spice):
        self.maxtimeout = 120
        self.spice = spice

    # compare rtp Alert messages (vlop, lop, oop)
    def compare_rtp_alerts(self, net, main_msg, sub_msg, time_out=90):
        self.spice.wait_for(HeaderID, time_out)
        ui_screen_main_msg = self.spice.query_item(HeaderID, 1)["text"]
        logging.info(f'Ui screen main message: {ui_screen_main_msg}')
        expected_msg = LocalizationHelper.get_string_translation(net, main_msg)
        # Main Message verification
        assert ui_screen_main_msg == expected_msg, 'Main Message displayed incorrectly'

        ui_screen_sub_msg = self.spice.query_item(SubHeaderMsgIDtxt, 2)["text"]
        logging.info(f'Ui screen sub message: {ui_screen_sub_msg}')
        expected_sub_msg = LocalizationHelper.get_string_translation(net, sub_msg)
        # sub Message verification
        assert ui_screen_sub_msg == expected_sub_msg, 'Sub Message displayed incorrectly'


