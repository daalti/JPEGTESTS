#########################################################################################
# @file     TraysAppProSelectUIOperations.py
# @authors  Mohammed Haris(mohammed.haris@hp.com)
# @date     01-06-2023
# @brief    Implementation for all the Trays navigation and Function methods
# (c) Copyright HP Inc. 2020. All rights reserved.
###########################################################################################
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import logging

from dunetuf.ui.uioperations.BaseOperations.ITraysAppUIOperations import ITraysAppUIOperations

class TraysAppProSelectUIOperations(ITraysAppUIOperations):
    
    button_tray = "#trayConfigurationView #SpiceButton"
    button_media_size_settings = "#trayInformationModel #SpiceButton"
    radio_button_a5 = "#PrintMediaSizeButtoniso_a5_148x210mm"
    radio_buttom_a5_rotated = "#PrintMediaSizeButtoncom_dot_hp_dot_ext_dot_mediaSize_dot_iso_a5_148x210mm_dot_rotated"

    view_tray_configuration = "#trayConfigurationView"
    view_tray_details = "#trayInformationModel"
    view_media_size_selection = "#mediaSelectionView"


    def __init__(self, spice):
        self.maxtimeout = 60
        self._spice = spice

    def goto_tray1(self):
        '''
        Navigates to Tray1 from Home Screen
        UI Flow is Home->Menu->Trays->Tray1
        '''
        self._spice.homeMenuUI().goto_menu_trays(self._spice)
        currentScreen = self._spice.wait_for(self.view_tray_configuration)
        currentScreen.mouse_wheel(180,180)
        self._spice.query_item(self.button_tray, 1).mouse_click()
        assert self._spice.wait_for(self.view_tray_details)
        time.sleep(1)
    
    def goto_tray2(self):
        '''
        Navigates to Tray2 from Home Screen
        UI Flow is Home->Menu->Trays->Tray1
        '''
        self._spice.homeMenuUI().goto_menu_trays(self._spice)
        currentScreen = self._spice.wait_for(self.view_tray_configuration)
        currentScreen.mouse_wheel(180,180)
        currentScreen.mouse_wheel(180,180)
        self._spice.query_item(self.button_tray, 2).mouse_click()
        assert self._spice.wait_for(self.view_tray_details)
        time.sleep(1)

    def modify_tray_size_letter(self):
        self._spice.homeMenuUI().menu_navigation(self._spice, "#DescriptiveButtonListLayout", "#MediaSizeButton")
        self._spice.homeMenuUI().menu_navigation(self._spice, "#RadioButtonListLayout", "#PrintMediaSizeButtonna_letter_8_dot_5x11in")

    def modify_tray_type_plain(self):
        self._spice.homeMenuUI().menu_navigation(self._spice, "#DescriptiveButtonListLayout", "#MediaTypeButton")
        self._spice.homeMenuUI().menu_navigation(self._spice, "#SpiceRadioButtonList", "#PrintMediaTypeButtonstationery")

    def goto_modifyTray(self):
        '''
        ProSelect goto_modifyTray() stub regarding
        design differences between proSelect and Workflow
        '''
        print("Do nothing ProSelect goto_modifyTray")

    def finish_modifyTray(self):
        '''
        ProSelect finish_modifyTray() stub regarding
        design differences between proSelect and Workflow
        '''
        print("Do nothing ProSelect finish_modifyTray")

    def verify_tray_media_size_string_a5_and_a5_rotated(self):
        '''
        Verify tray media sizes a5 and a5 rotated have the expected string
        UI Should be in the specific Tray screen
        '''
        print("Click on Media Size Option")

        currentScreen = self._spice.wait_for(self.view_tray_details)
        currentScreen.mouse_wheel(180,180)
        self._spice.query_item(self.button_media_size_settings, 1).mouse_click()
        self._spice.wait_for(self.view_media_size_selection)

        print("verify a5 paper size has no junk charecters")
        self._spice.homeMenuUI().menu_navigation(self._spice, self.view_media_size_selection, self.radio_button_a5, selectOption=False)
        actual_text = self._spice.query_item(self.radio_button_a5 +" RadioButton")["text"]
        assert actual_text == 'A5 (148x210 mm)', "Mismatch observed in A5 media size"

        print("verify a5 rotated paper size has no junk charecters")
        self._spice.homeMenuUI().menu_navigation(self._spice, self.view_media_size_selection, self.radio_buttom_a5_rotated, selectOption=False)
        actual_text = self._spice.query_item(self.radio_buttom_a5_rotated + " RadioButton")["text"]
        assert actual_text == 'A5 ▭ (148x210 mm)', "Mismatch observed in A5 rotated media size"

    
