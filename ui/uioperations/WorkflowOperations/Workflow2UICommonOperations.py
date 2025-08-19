import sys
import time
import logging
import json
import os

from dunetuf.ui.uioperations.BaseOperations.IWorkflowUICommonOperations import IWorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.qmltest.QmlTestServer import QmlItemNotFoundError
from dunetuf.ui.uioperations.WorkflowOperations.JamAutoNavUIObjectIds import JamAutoNavUIObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations
from dunetuf.ui.uioperations.WorkflowOperations.HomeAppWorkflowObjectIds import HomeAppWorkflowObjectIds

class Workflow2UICommonOperations(WorkflowUICommonOperations):

    def __init__(self, spice):
        '''
        spice : spice is an UI fixture
        '''
        self._spice = spice
        self.maxtimeout = 120

    def validateObjectVisibility(self, listObj, rowObject, elementObject, isVertical):

        """
        Validate object if it is visible

        Args:
            objectApp: Param1 -- Base object (can be list object),
                        Param2 -- Object within Base (can be row object),
                        Param3 -- Individual object with in Param2 (can be an object in row)
                        Param4 -- 1(Vertical), 0(Horizontal)
        """

        logging.info("----------------############------------------------")

        isEnabled = False

        item = self._spice.check_item(listObj + " " + rowObject+ " " + elementObject)
        if item != None:
            isEnabled = item["visible"]
            logging.info("isEnabled: %s", str(isEnabled))
            if (isEnabled is False):
                return isEnabled
        else:
            logging.info(listObj + " " + rowObject+ " " + elementObject+" not found")
        return isEnabled

    def scroll_to_position_horizontal(self, position: int) -> None:
        '''
        Scrolls to the provided position
        Parameters:
        spice: the spice object
        position: between 0 and max swipeview pages
        '''
        self._spice.query_item(HomeAppWorkflowObjectIds.home_swipe_view)["currentIndex"] = 0

    def scroll_to_home_page(self, swipe_view: str, index: int) -> None:
        """
        Scrolls vertically when the scrollbar is not visible or the object name is unknown, then clicks the desired button
        Parameters:
            -> spice: the spice object
            -> swipe_view: object name of the swipe view which has pages
            -> index: index of the page to be scrolled to
        """
        # Get the swipeView object using swipe_view object name
        swipe_view_object = self._spice.query_item(swipe_view)

        # Set the currentIndex to index parameter
        swipe_view_object["currentIndex"] = index
        time.sleep(2)

    def find_item_across_pages(self, swipe_view_id: str, object_id: str) -> int:
        #Search for an item across the pages
        try:
            swipe_view = self._spice.query_item(swipe_view_id)
            max_pages = swipe_view["count"]
            original_page = swipe_view["currentIndex"]
            navigation_count = 0
            if "#" in object_id:
                clean_id = object_id.split("#")[1]
            else:
                clean_id = object_id
                
            for page in range(max_pages):
                swipe_view["currentIndex"] = page
                navigation_count += 1
                time.sleep(2)
                try:
                    item = self._spice.check_item(object_id)
                    if item and item.get("visible", False):
                        swipe_view["currentIndex"] = original_page
                        navigation_count += 1
                        return page
                except Exception as e:
                    logging.debug(f"Error checking for {object_id} on page {page}: {str(e)}")
            swipe_view["currentIndex"] = original_page
            navigation_count += 1
            return -1
            
        except Exception as e:
            logging.debug(f"Error in find_item_across_pages: {str(e)}")
            return -1