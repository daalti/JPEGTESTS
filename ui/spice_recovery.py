import sys
import logging
import time

from dunetuf.qmltest.QmlTestServer import QmlTestServer
from dunetuf.dial import DialController
from dunetuf.udw import DuneUnderware
from dunetuf.cdm import CDM
from dunetuf.ui.spice_home_app import spice_home_app
from dunetuf.ui.spice_signin_app import spice_signin_app
from dunetuf.ui.spice_network_app import spice_network_app
from dunetuf.ui.spice_common_operations import spice_common_operations
from dunetuf.ui.spice_service_app import spice_service_app
from dunetuf.ui.spice_tools_app import spice_tools_app
from dunetuf.ui.spice_keyboard_app import spice_keyboard_app
from dunetuf.ui.spice_firmware_update_app import spice_firmware_update_app
from dunetuf.ui.spice_substrate_library_app import spice_substrate_library_app
from dunetuf.ui.uioperations.PomOperations.NetworkApp.NetworkAppPage import NetworkAppPage


class Spice_recovery(QmlTestServer, DialController, spice_home_app, spice_signin_app, spice_network_app, 
                spice_common_operations, spice_service_app, spice_tools_app, spice_firmware_update_app, 
                spice_substrate_library_app, spice_keyboard_app):

    def __init__(self, addr: str, port: int, default_timeout: float = 5.0) -> None:

        self.maxtimeout = 60
        self.ipaddress = addr
        self._uiType = None
        self._uiSize = None
        self._uiTheme = None
        self.cdm = CDM(addr)
        self._networkAppPage = None
        self._firmwareUpdateAppPage = None
        self._substrateLibraryAppPage = None

        QmlTestServer.__init__(self, addr, port)
        DialController.__init__(self, addr)
        self.udw = DuneUnderware(self.ipaddress)
        spice_home_app.__init__(self, self.uitype, self.uisize)
        spice_signin_app.__init__(self, self.uitype, self.uisize)
        spice_network_app.__init__(self, self.uitype, self.uisize)
        spice_common_operations.__init__(self, self.uitype, self.uisize)
        spice_service_app.__init__(self, self.uitype, self.uisize)
        spice_tools_app.__init__(self, self.uitype, self.uisize)
        spice_firmware_update_app.__init__(self, self.uitype, self.uisize)
        spice_substrate_library_app.__init__(self, self.uitype, self.uisize)

        logging.debug('Control Panel Experience is: %s', self.udw.mainUiApp.ControlPanel.getExperience())

    def wait_ready(self, timeout=60):
        """Check if UI is ready.

        A screenshot request is sent to check for connectivity.

        Args:
            timeout: Maximum wait time (s).
        """

        ready = False
        started = time.time()
        while not ready:
            if time.time() - started > timeout:
                raise TimeoutError("UI not ready within expected time")

            try:
                r = self.request("screenshot", stream=True)
            except ConnectionError:
                ready = False
            else:
                print("wait ready")
                if r and "status" in r:
                    if r["status"] == "Success":
                        ready = True

            if not ready:
                time.sleep(1)

    @property
    def uitype(self):
        if self._uiType == None:
            self._uiType = self.udw.mainUiApp.ControlPanel.getExperience()
        return self._uiType

    @property
    def uisize(self):
        if self._uiSize == None:
            self._uiSize = self.udw.mainUiApp.ControlPanel.getBreakPoint()
        return self._uiSize

    @property
    def uitheme(self):
        if self._uiTheme == None:
            self._uiTheme = self.udw.mainUiApp.ApplicationEngine.getTheme()
        return self._uiTheme

    def scroll_home_right(self, delta: float = 0.2):
        scrollbar = self.wait_for('#hScrollhorizontalScroll')
        scrollbar.scroll_right(delta)

    def scroll_home_left(self, delta: float = 0.2):
        scrollbar = self.wait_for('#hScrollhorizontalScroll')
        scrollbar.scroll_left(delta)


    # Avoid until n SystemErrors in screen clicking OK buttons
    def clickSystemEventsOKButtons(self, index: int = 0):
        # MAX number os SystemEvent screens accepted
        maxSystemEventScreens = 10

        object = self.query_item("#FooterViewRight #OK", index)

        try:
            # Wait for clickable situation
            self.wait_until(lambda: object["enabled"] == True)
            self.wait_until(lambda: object["visible"] == True)

            # Validate object Button and click it
            assert object["enabled"] == True, "Button is not enabled"
            assert object["visible"] == True, "Button is not visible"

        except:
            if index < maxSystemEventScreens:
                self.clickSystemEventsOKButtons(index + 1)

        finally:
            # Click on the middle of the object
            middle_width = object["width"] / 2
            middle_height = object["height"] / 2
            object.mouse_click(middle_width, middle_height)

    def cleanSystemEventAndWaitHomeScreen(self, timeout=120):
        homeScreen = self.is_HomeScreen()
        counting_time = 0

        while homeScreen == False:
            # Check SystemEvent screen, click OK button if exists
            logging.info("!We dont have homeScreen, check for a SystemEvent and dismiss screen clicking OK button")

            try:
                self.clickSystemEventsOKButtons()

            except:
                logging.info("We are not in warning SystemError screen")
            finally:
                homeScreen = self.is_HomeScreen()
                assert counting_time != timeout
                counting_time = counting_time + 10
                time.sleep(10)

        return True

    # return the statusCenter index where the alarm is present
    def check_alert_text(self, text):
        self.wait_for("#AlertTitle")
        i = 0
        found = False
        while not found:
            alertText = self.query_item("#AlertTitle", i)
            logging.info("text=%s", alertText["text"])
            # Discard System Errors. We want the first alarm in status Center
            if str(alertText["text"]).find('Event Code:') == -1:
                found = True
                assert str(alertText["text"]) == str(text)
            else:
                found = False
                i = i + 1
        return i

    def check_error_icon(self, index):
        self.wait_for("#AlertIcon")
        alertIcon = self.query_item("#AlertIcon", index)
        logging.info("source=%s", alertIcon["source"])
        assert str(alertIcon["source"]) == str("qrc:/images/Status/Error.json")

    def check_warning_icon(self, index):
        self.wait_for("#AlertIcon")
        alertIcon = self.query_item("#AlertIcon", index)
        logging.info("source=%s", alertIcon["source"])
        assert str(alertIcon["source"]) == str("qrc:/images/Status/Warning.json")

    def check_informative_icon(self, index):
        self.wait_for("#AlertIcon")
        alertIcon = self.query_item("#AlertIcon", index)
        logging.info("source=%s", alertIcon["source"])
        assert str(alertIcon["source"]) == str("qrc:/images/Status/Informative.json")

    @property
    def network_app(self):
        ''' Get Network app '''
        if self._networkAppPage == None:
            self._networkAppPage = NetworkAppPage(self)
        return self._networkAppPage

    @property
    def menu_app(self):
        ''' Get Menu app '''
        if self._menuAppPage == None:
            self._menuAppPage = MenuAppPage(self)
        return self._menuAppPage

    @property
    def info_app(self):
        ''' Get Info app '''
        if self._infoAppPage == None:
            self._infoAppPage = InfoAppPage(self)
        return self._infoAppPage


    @property
    def substrate_library_app(self):
        ''' Get Gallery app '''
        if self._substrateLibraryAppPage == None:
            self._substrateLibraryAppPage = SubstrateLibraryAppPage(self)
        return self._substrateLibraryAppPage

    def validate_app(self, object_app, wait_until_enabled=True):
        """
        Waits for an object and checks is visible and enabled

        Args:
            spice: ui fixture
            object_app: object to check
            wait_until_enabled: wait until the object is enabled.(Default=True)
        """
        if wait_until_enabled:
            self.wait_until(lambda: object_app["enabled"] is True)

        assert object_app["visible"] is True, "App Screen View is not visible"
        assert object_app["enabled"] is True, "App Screen View is not enabled"

    def validate_button(self, button, is_visible=True, is_enabled=True):
        """
        Validates the visible/enabled properties of an object.
        """
        self.wait_until(lambda: button["visible"] == is_visible)
        self.wait_until(lambda: button["enabled"] == is_enabled)

    def statusCenter_dashboard_expand(self):
        """
        Performs a mouse_click on status center dashboard
        to expand it when collapsed
        """
        if self.uitype == "Workflow2":
            pass #Workflow2 there is no status center
        if self.uitype == "Workflow":
            statusCenter = self.wait_for("NotificationCenterView")
        
            if statusCenter["state"] != "EXPANDED":
                statusCenterDash = self.wait_for("NotificationCenterView #footer #footerRectangle")
    
                middle_width  = statusCenterDash["width"] / 2
                middle_height = statusCenterDash["height"] / 2

                statusCenterDash.mouse_click(middle_width, middle_height)
                time.sleep(3)

    def statusCenter_dashboard_collapse(self):
        """
        Performs a mouse_click on status center dashboard
        to collapse it when expanded
        """
        if self.uitype == "Workflow2":
            pass #Workflow2 there is no status center
        if self.uitype == "Workflow":
            statusCenter = self.wait_for("NotificationCenterView")
        
            if statusCenter["state"] != "COLLAPSED":
                statusCenterDash = self.wait_for("NotificationCenterView #footer #footerRectangle")
    
                middle_width  = statusCenterDash["width"] / 2
                middle_height = statusCenterDash["height"] / 2

                statusCenterDash.mouse_click(middle_width, middle_height)
                time.sleep(3)
