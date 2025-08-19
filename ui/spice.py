import sys
import logging
import time

from dunetuf.qmltest.QmlTestServer import QmlTestServer, QmlItemNotFoundError

from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.dial import DialController
from dunetuf.udw import DuneUnderware
from dunetuf.cdm import CDM
from dunetuf.ui.spice_home_app import spice_home_app
from dunetuf.ui.spice_yeti_app import spice_yeti_app
from dunetuf.ui.spice_menu_app import spice_menu_app
from dunetuf.ui.spice_fax_app import spice_fax_app
from dunetuf.ui.spice_copy_app import spice_copy_app
from dunetuf.ui.spice_signin_app import spice_signin_app
from dunetuf.ui.spice_folder_widget import spice_folder_widget
from dunetuf.ui.spice_network_app import spice_network_app
from dunetuf.ui.spice_info_app import spice_info_app
from dunetuf.ui.spice_wifi_app import spice_wifi_app
from dunetuf.ui.spice_scan_app import spice_scan_app
from dunetuf.ui.spice_status_center import spice_status_center
from dunetuf.ui.spice_contacts_app import spice_contacts_app
from dunetuf.ui.spice_job_app import spice_job_app
from dunetuf.ui.spice_job_storage_app import spice_job_storage_app
from dunetuf.ui.spice_oobe_app import spice_oobe_app
from dunetuf.ui.spice_copy_idcard_app import spice_copy_idcard_app
from dunetuf.ui.spice_print_app import spice_print_app
from dunetuf.ui.spice_common_operations import spice_common_operations
from dunetuf.ui.spice_supplies_app import spice_supplies_app
from dunetuf.ui.spice_media_app import spice_media_app
from dunetuf.ui.spice_service_app import spice_service_app
from dunetuf.ui.spice_tools_app import spice_tools_app
from dunetuf.ui.spice_keyboard_app import spice_keyboard_app
from dunetuf.ui.spice_firmware_update_app import spice_firmware_update_app
from dunetuf.ui.spice_substrate_library_app import spice_substrate_library_app
from dunetuf.ui.spice_quickset_app import spice_quickset_app
from dunetuf.ui.spice_trays_app import spice_trays_app
from dunetuf.ui.uioperations.PomOperations.ScanUsbApp.ScanUsbAppPage import ScanUsbAppPage
from dunetuf.ui.uioperations.PomOperations.ScanDiskApp.ScanDiskAppPage import ScanDiskAppPage
from dunetuf.ui.uioperations.PomOperations.CopyApp.CopyAppPage import CopyAppPage
from dunetuf.ui.uioperations.PomOperations.NetworkApp.NetworkAppPage import NetworkAppPage
from dunetuf.ui.uioperations.PomOperations.JobQueueApp.JobQueueAppPage import JobQueueAppPage
from dunetuf.ui.uioperations.PomOperations.MediaApp.MediaAppPage import MediaAppPage
from dunetuf.ui.uioperations.PomOperations.SuppliesApp.SuppliesAppPage import SuppliesAppPage
from dunetuf.ui.uioperations.PomOperations.MainApp.MainAppPage import MainAppPage
from dunetuf.ui.uioperations.PomOperations.MenuApp.MenuAppPage import MenuAppPage
from dunetuf.ui.uioperations.PomOperations.InfoApp.InfoAppPage import InfoAppPage
from dunetuf.ui.uioperations.PomOperations.GalleryApp.GalleryAppPage import GalleryAppPage
from dunetuf.ui.uioperations.PomOperations.SubstrateLibraryApp.SubstrateLibraryAppPage import SubstrateLibraryAppPage
from dunetuf.ui.uioperations.PomOperations.SignInApp.SignInAppPage import SignInAppPage
from dunetuf.ui.uioperations.PomOperations.SignInApp.HomePageApp import HomePageApp
from dunetuf.ui.uioperations.PomOperations.SignInApp.HomePageAppProSelect import HomePageAppProSelect
from dunetuf.ui.uioperations.PomOperations.SignInApp.SignInAppPageProSelect import SignInAppPageProSelect
from dunetuf.ui.uioperations.PomOperations.StatusCenterApp.StatusCenterApp import StatusCenterApp
from dunetuf.ui.uioperations.PomOperations.FaxApp.FaxAppPage import FaxAppPage
from dunetuf.ui.uioperations.PomOperations.JobsApp.JobsAppPage import JobsAppPage
from dunetuf.ui.uioperations.PomOperations.MenuApp.MenuAppConstructor import MenuAppConstructor
from dunetuf.ui.uioperations.PomOperations.CopyApp.CopyApp import CopyApp
from dunetuf.ui.uioperations.PomOperations.MenuApp.MenuApp import MenuApp
from dunetuf.ui.uioperations.PomOperations.SettingsApp.SettingsAppPage import SettingsAppPage
from dunetuf.ui.uioperations.PomOperations.ToolsApp.ToolsAppPage import ToolsAppPage
from dunetuf.ui.uioperations.PomOperations.ServiceApp.ServiceAppPage import ServiceAppPage
from dunetuf.ui.uioperations.PomOperations.SignInApp.UniversalSignInWrapper import UniversalSignInWrapper
from dunetuf.ui.uioperations.PomOperations.QuicksetsApp.QuicksetsApp import QuicksetsApp
from dunetuf.ui.uioperations.PomOperations.ScanToEmailApp.ScanToEmailApp import ScanToEmailApp

class Spice(QmlTestServer, DialController, spice_home_app, spice_menu_app, spice_fax_app, spice_copy_app,
            spice_signin_app, spice_folder_widget , spice_network_app, spice_info_app, spice_wifi_app, spice_scan_app, spice_status_center, spice_job_app, spice_job_storage_app,
            spice_oobe_app, spice_copy_idcard_app, spice_print_app, spice_common_operations, spice_supplies_app,
            spice_media_app, spice_service_app, spice_contacts_app, spice_tools_app, spice_firmware_update_app, spice_yeti_app,
            spice_substrate_library_app, spice_keyboard_app, spice_quickset_app, spice_trays_app):

    def __init__(self, addr: str, port: int, screencapture: bool = False, default_timeout: float = 5.0) -> None:

        self.maxtimeout = 60
        self.maxQueryIndex = 32767
        self.ipaddress = addr
        self._uiType = None
        self._uiSize = None
        self._uiTheme = None
        self.cdm = CDM(addr)
        self._scanUsbAppPage = None
        self._scanDiskAppPage = None
        self._copyAppPage = None
        self._networkAppPage = None
        self._jobQueueAppPage = None
        self._mediaAppPage = None
        self._suppliesAppPage = None
        self._mainAppPage = None
        self._menuAppPage = None
        self._infoAppPage = None
        self._galleryAppPage = None
        self._substrateLibraryAppPage = None
        self._signInAppPage = None
        self._signInAppPageProSelect = None
        self._statusCenterPage = None
        self._homeAppPage = None
        self._homeAppPageProSelect = None
        self._status_center = None
        self._faxAppPage = None
        self._jobsAppPage = None
        self._menuApp = None
        self._settingsAppPage = None
        self._toolsAppPage = None
        self._serviceAppPage = None
        self._universalSignInAppWrapper = None
        self._copyApp = None
        self._quicksetsApp = None
        self._scanToEmailApp = None

        QmlTestServer.__init__(self, addr, port, screencapture)
        DialController.__init__(self, addr)
        self.udw = DuneUnderware(self.ipaddress)
        spice_home_app.__init__(self, self.uitype, self.uisize)
        spice_yeti_app.__init__(self, self.uitype, self.uisize)
        spice_menu_app.__init__(self, self.uitype, self.uisize)
        spice_fax_app.__init__(self, self.uitype, self.uisize)
        spice_copy_app.__init__(self, self.uitype, self.uisize)
        spice_signin_app.__init__(self, self.uitype, self.uisize)
        spice_folder_widget.__init__(self, self.uitype, self.uisize)
        spice_network_app.__init__(self, self.uitype, self.uisize)
        spice_info_app.__init__(self, self.uitype, self.uisize)
        spice_wifi_app.__init__(self, self.uitype, self.uisize)
        spice_scan_app.__init__(self, self.uitype, self.uisize)
        spice_contacts_app.__init__(self, self.uitype, self.uisize)
        spice_job_app.__init__(self, self.uitype, self.uisize)
        spice_job_storage_app.__init__(self, self.uitype, self.uisize)
        spice_oobe_app.__init__(self, self.uitype, self.uisize)
        spice_copy_idcard_app.__init__(self, self.uitype, self.uisize)
        spice_print_app.__init__(self, self.uitype, self.uisize)
        spice_common_operations.__init__(self, self.uitype, self.uisize)
        spice_supplies_app.__init__(self, self.uitype, self.uisize)
        spice_media_app.__init__(self, self.uitype, self.uisize)
        spice_service_app.__init__(self, self.uitype, self.uisize)
        spice_tools_app.__init__(self, self.uitype, self.uisize)
        spice_firmware_update_app.__init__(self, self.uitype, self.uisize)
        spice_substrate_library_app.__init__(self, self.uitype, self.uisize)
        spice_keyboard_app.__init__(self, self.uitype, self.uisize)
        spice_quickset_app.__init__(self, self.uitype, self.uisize)
        spice_trays_app.__init__(self, self.uitype, self.uisize)

        logging.debug('Control Panel Experience is: %s', self.udw.mainUiApp.ControlPanel.getExperience())

        currentState = int(self.udw.mainApp.ActivityMonitor.getCurrentState().split(" ")[1])
        logging.debug('Printer Sleep status is: %s', currentState)
        if currentState >= 2:
            logging.debug("Waking up printer")
            self.udw.mainApp.execute("ActivityMonitor PUB_notifyUserActivity 1")
        currentState = int(self.udw.mainApp.ActivityMonitor.getCurrentState().split(" ")[1])
        if currentState <= 1:
            logging.debug("Printer awake now")
        cdmconfig = self.cdm.get('/cdm/power/v1/constraints')
        logging.info(f'The cdm data is <{cdmconfig}>')
        data_options_sleepTimeout = None

        for item in cdmconfig['validators']:
            if (item.get("propertyPointer", None) == "/sleepTimeout") and (item.get("options", None)):
                data_options_sleepTimeout = item['options']
            elif (item.get("propertyPointer", None) == "/sleepTimeout") and (item.get("max", None)):
                data_options_sleepTimeout = item['max']

        if any('iValue' in d for d in data_options_sleepTimeout):
            sleepTimeout_values = [d['iValue'] for d in data_options_sleepTimeout]
            max_sleepTimeoutValue = max(sleepTimeout_values)
        else:
            sleepTimeout_values = data_options_sleepTimeout['value']
            max_sleepTimeoutValue = sleepTimeout_values

        logging.info(f'The applicable sleepTimeout values are <{max_sleepTimeoutValue}>')

        self.cdm.patch_raw('/cdm/power/v1/configuration', {"sleepTimeout": max_sleepTimeoutValue})
        logging.debug('Setting the sleepTimeout value to the maximum value supported by the device')

        # current system activity default time out is 60s, it means that the print will return to Home screen when printer inactive time out at non Home screen
        if self.udw.mainUiApp.ApplicationEngine.isInactivityTimerSupported():
            logging.debug('Set system activity to 18000 sec to make sure printer has enough inactive time out during script execution')
            self.udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(18000)

        logging.debug('Setting device language to english')
        self.cdm.patch_raw('cdm/system/v1/configuration', {"deviceLanguage": "en"})

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

    def goto_homescreen(self):
        # Printer goes into sleep mode once cdm/ews calls[that execution time is greater than sleep time] in test before UI navigation, for
        # this scenario need to check printer in sleep or not when perform UI navigation
        currentState = int(self.udw.mainApp.ActivityMonitor.getCurrentState().split(" ")[1])
        logging.debug('Printer Sleep status is: %s',currentState)
        if currentState >= 2:
            logging.debug("Waking up printer")
            self.udw.mainApp.execute("ActivityMonitor PUB_notifyUserActivity 1")
            time.sleep(2)
            
        #Hide the keyboard on S and XS screens before navigating, as header and footer are hidden when the keyboard is visible.        
        self.dismiss_keyboard()

        # Note: Need to acknowledge few alerts to get device UI into home screen.
        try:
            alerts = self.get_alerts()
            for alert in alerts:
                if alert['action'] in ["ok", "cancel", "okButtonUi", "clear"]:
                    data = {"selectedAction" : alert['action']}
                    result = self.cdm.put_raw(alert['href'],data)
                    assert 200 == result.status_code,"Failed to clear the {0} prompt".format(alert['action'])
        except:
            logging.debug("Failed to clear the alerts")
            cdm_alerts = self.cdm.get(self.cdm.ALERTS)['alerts']
            logging.debug("Alerts reported:{0}".format(cdm_alerts))

        # TODO currently the code supports ProSelect and Workflow  control panels.
        if self.uitype == "ProSelect":
            if self.uitheme == "hybridTheme":
                try:
                    logging.info("Using Keyhandler UDW command for HOME Button: Hybrid UI")
                    self.udw.mainUiApp.KeyHandler.setKeyPress("HOME")
                    assert self.is_HomeScreen(), 'Not at Home Screen'
                    logging.info("At Home Screen")
                except:
                    logging.exception("Caught exception in goto_homescreen")
                    return False
            else:
                if self.is_longpressmenu():
                    longPressApp = self.wait_for("#LongPressLayout")
                    startTime = time.time()
                    timeSpentWaiting = time.time() - startTime
                    # scroll till you reach the close button
                    while (self.query_item("#CloseButton")["activeFocus"] == False and timeSpentWaiting < self.maxtimeout):
                        longPressApp.mouse_wheel(0, 0)
                        timeSpentWaiting = time.time() - startTime
                        time.sleep(1)
                    closeButton = self.wait_for("#CloseButton SpiceText")
                    closeButton.mouse_click()
                if not self.is_HomeScreen():
                    try:
                        logging.info("Navigating to Home Screen")
                        # long press for the navigation menu
                        navigationApp = self.query_item("#CurrentAppText")
                        navigationApp.mouse_press(0, 0, QmlTestServer.MOUSE_BTN.MIDDLE)
                        longPressApp = self.wait_for("#LongPressLayout")
                        logging.info("At Long Press Menu")
                        time.sleep(1)
                        startTime = time.time()
                        timeSpentWaiting = time.time() - startTime
                        # scroll till you reach the home button
                        while (self.query_item("#HomeButton")["activeFocus"] == False and timeSpentWaiting < self.maxtimeout):
                            longPressApp.mouse_wheel(180, 180)
                            timeSpentWaiting = time.time() - startTime
                            time.sleep(1)
                        assert self.wait_for("#HomeButton")["activeFocus"] == True, '#HomeButton not found'
                        homeButton = self.wait_for("#HomeButton SpiceText")
                        homeButton.mouse_click()
                        logging.debug("#HomeButton clicked")
                        # make sure that you are in the home screen
                        self.wait_for("#HomeScreenView")
                        homeApp = self.query_item("#HomeScreenView")
                        assert self.is_HomeScreen(), 'Not at Home Screen'
                        logging.info("At Home Screen")
                    except:
                        logging.exception("Caught exception in goto_homescreen")
                        return False
        elif self.uitype in ["Workflow","Workflow2"]:
            if not self.is_HomeScreen():
                try:
                    self.statusCenter_dashboard_collapse()
                except:
                    pass
                logging.info("Navigating to Home Screen")
                try:
                    if self.uisize == "XS":
                        self.common_operations.click_home_button()
                    else:
                        homeButton = self.wait_for("#HomeButton[visible=true]", query_index=self.maxQueryIndex)
                        # homeButton = self.wait_for("#HomeButton", query_index=self.maxQueryIndex)
                        time.sleep(1)
                        homeButton.mouse_click()
                    time.sleep(2)
                    # make sure that you are in the home screen
                    assert self.is_HomeScreen(), 'Not at Home Screen'
                    logging.info("At Home Screen")
                except Exception as e:
                    logging.exception("Caught exception in goto_homescreen: {}".format(e))
                    return False
            else:
                logging.info("Already in home screen")
        else:
            raise NotImplementedError('Unimplemented method  %s' % sys._getframe().f_code.co_name)

    def click_backButton(self):
        if self.uisize == "XS":
            self.common_operations.click_back_button()
        else:
            if self.uitype == "ProSelect":
                backButton = self.wait_for("#BackButton SpiceText")
            else:
                backButton = self.check_item("#BackButton[visible=true]",query_index=self.maxQueryIndex)
                if backButton == None:
                    return False
            middle_width  = backButton["width"] / 2
            middle_height = backButton["height"] / 2
            backButton.mouse_click(middle_width, middle_height)
            logging.info("#BackButton clicked")
        return True

    def goto_homescreen_back_button(self):
        startTime = time.time()
        timeSpentWaiting = time.time() - startTime
        maxtimeout = 120
        homeScreen = False

        while homeScreen == False and (timeSpentWaiting < maxtimeout):
            homeScreen = self.is_HomeScreen()
            if homeScreen:
                return
            # Click on BackButton
            isSuccess = self.click_backButton()
            logging.debug("click_backButton is successful : {0}".format(isSuccess))
            if isSuccess and self.uisize == "XS":
                # Back button is disabled in Menu screen.
                if self.check_item("#AdminAppApplicationStackView #SpiceHeaderVar2 #SpiceHeaderVar2HeaderView SpiceText[visible=true]")["text"] == "Menu":
                    logging.debug("Found Menu screen and Back button is disabled on the screen, use Home button to navigate to Home screen.")
                    self.common_operations.click_home_button()
                homeScreen = self.is_HomeScreen()
                if homeScreen:
                    return
            elif not isSuccess and self.uitype in ["Workflow", "Workflow2"]:
                homeButton = self.check_item("#AdminAppApplicationStackView #SpiceBreadcrumb #HomeButton[visible=true]")
                if homeButton != None:
                    logging.info("At the AdminScreen ")
                    homeButton.mouse_click()
                    homeScreen = self.is_HomeScreen()
                    if homeScreen:
                        return
                else:
                    logging.info("At the AdminScreen but HomeScreen Button not Found")
            timeSpentWaiting = time.time() - startTime
        if homeScreen == False:
            assert False

    def is_HomeScreen(self) -> bool:
        try:
            self.wait_until(lambda: self.request("isOnHomeScreen") == True, timeout=10, delay=1)
            logging.info("At the Homescreen")
            return True
        except Exception:
            logging.debug("Not in the Homescreen")
            logging.debug("Alerts Found : " + str(self.cdm.get(self.cdm.ALERTS)['alerts']))
            return self.is_floatingDockHomeScreen(timeout=0, focus_timeout=0)

    def is_floatingDockHomeScreen(
        self,
        timeout=QmlTestServer.WAIT_TIMEOUT,
        focus_timeout=QmlTestServer.UNTIL_TIMEOUT,
    ) -> bool:
        try:
            homeApp = self.wait_for("#floatingDock", timeout=timeout)
            self.wait_until(
                lambda: homeApp["activeFocus"] == True, timeout=focus_timeout
            )
            logging.info("At the floatingDock Homescreen")
            return True
        except Exception:
            logging.info("Not in the floatingDock Homescreen")
            return self.is_widgetsHomeScreen(timeout=0, focus_timeout=0)

    def is_widgetsHomeScreen(
        self,
        timeout=QmlTestServer.WAIT_TIMEOUT,
        focus_timeout=QmlTestServer.UNTIL_TIMEOUT,
    ) -> bool:
        try:
            widgetApp = self.wait_for("#widgetsLoader", timeout=timeout)
            self.wait_until(
                lambda: widgetApp["activeFocus"] == True, timeout=focus_timeout
            )
            logging.info("At the Widgets Homescreen")
            return True
        except Exception:
            logging.info("Not in the Widgets Homescreen")
            return self.is_homeDockHomeScreen(timeout=0, focus_timeout=0)

    def is_homeDockHomeScreen(
        self,
        timeout=QmlTestServer.WAIT_TIMEOUT,
        focus_timeout=QmlTestServer.UNTIL_TIMEOUT,
    ) -> bool:
        try:
            homeDock = self.wait_for("#homeDock", timeout=timeout)
            self.wait_until(
                lambda: homeDock["activeFocus"] == True, timeout=focus_timeout
            )
            logging.info("At the homeDock Homescreen")
            return True
        except Exception:
            logging.info("Not in the homeDock Homescreen")
            return False

    def is_longpressmenu(self) -> bool:
        try:
            self.query_item("#LongPressLayout")
            logging.info("At the Long Press Menu")
            return True
        except:
            logging.info("Not in the Long Press Menu")
            return False

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
        homeScreen: bool = self.is_HomeScreen()

        start_time = time.time()
        while not homeScreen:
            # Check SystemEvent screen, click OK button if exists
            logging.info(
                "!We dont have homeScreen, "
                "check for a SystemEvent and dismiss screen clicking OK button"
            )

            try:
                self.clickSystemEventsOKButtons()
            except Exception:
                logging.info("We are not in warning SystemError screen")
                try:
                    self.query_item("#SystemEventErrorView")
                    logging.info(
                        "SystemEventErrorView: %s",
                        self.query_item("#titleObject")["text"],
                    )
                except Exception:
                    logging.info("Current screen is not SystemEventErrorView...")
            
            # Handle alerts that have a "Hide" button
            try:
                hide = self.query_item("#Hide")
                hide.mouse_click()
            except Exception:
                logging.info("No alerts with 'Hide' button")

            try:
                # Handling Sign in screen which doesn't have home button
                cancel = self.query_item("#userCancelButton")
                cancel.mouse_click()
            except Exception:
                # Navigating to homescreen when the screen
                # is not at home during the start of the test.
                self.goto_homescreen()

            finally:
                # is_HomeScreen adds a delay, do not add additional sleep steps
                homeScreen = self.is_HomeScreen()
                assert time.time() - start_time < timeout, "Timeout waiting for HomeScreen"

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

    def validate_active_focus(self, viewId, itemId):
        """
        This function is intended to be used by views where the
        buttons aren't activated until scrolling all the way to
        the bottom. The viewId is the screen that the item is on.
        The itemId is the element that you expect to get active focus.
        This will assert if the item doesn't get focus after it is
        enabled or when timeout seconds have elapsed.
        """
        view = self.wait_for(viewId)
        assert view
        timeout = 100
        startTime = time.time()
        # scroll down the page until the button becomes enabled
        while self.query_item(itemId)["enabled"] is False:
            elapsedTime = time.time() - startTime
            assert elapsedTime < timeout, f"Timed out waiting for {itemId} to become enabled!"

            view.mouse_wheel(180,180)
            time.sleep(1)
        # ensure that this is the item that gets active focus
        assert self.query_item(itemId)["activeFocus"] is True, "Expected item did not have active focus!"

    @property
    def status_center(self):
        ''' Get status center '''
        if self._status_center == None:
            spice_status_center.__init__(self, self.uitype, self.uisize)
            self._status_center = spice_status_center.status_center(self, self.cdm)
        return self._status_center

    @property
    def copy_app(self):
        ''' Get copy app '''
        if self._copyAppPage == None:
            self._copyAppPage = CopyAppPage(self)
        return self._copyAppPage

    @property
    def job_queue_app(self):
        ''' Get job queue app '''
        if self._jobQueueAppPage == None:
            self._jobQueueAppPage = JobQueueAppPage(self)
        return self._jobQueueAppPage

    @property
    def main_app(self):
        ''' Get main app '''
        if self._mainAppPage == None:
            self._mainAppPage = MainAppPage(self)
        return self._mainAppPage

    @property
    def media_app(self):
        ''' Get Media app '''
        if self._mediaAppPage == None:
            self._mediaAppPage = MediaAppPage(self)
        return self._mediaAppPage

    @property
    def network_app(self):
        ''' Get Network app '''
        if self._networkAppPage == None:
            self._networkAppPage = NetworkAppPage(self)
        return self._networkAppPage

    @property
    def scan_usb_app(self):
        ''' Get Scan Usb app '''
        if self._scanUsbAppPage == None:
            self._scanUsbAppPage = ScanUsbAppPage(self)
        return self._scanUsbAppPage

    @property
    def scan_disk_app(self):
        ''' Get Scan Disk app '''
        if self._scanDiskAppPage == None:
            self._scanDiskAppPage = ScanDiskAppPage(self)
        return self._scanDiskAppPage

    @property
    def supplies_app(self):
        ''' Get Supplies app '''
        if self._suppliesAppPage == None:
            self._suppliesAppPage = SuppliesAppPage(self)
        return self._suppliesAppPage

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
    def gallery_app(self):
        ''' Get Gallery app '''
        if self._galleryAppPage == None:
            self._galleryAppPage = GalleryAppPage(self)
        return self._galleryAppPage

    @property
    def substrate_library_app(self):
        ''' Get Gallery app '''
        if self._substrateLibraryAppPage == None:
            self._substrateLibraryAppPage = SubstrateLibraryAppPage(self)
        return self._substrateLibraryAppPage

    @property
    def sign_in_app(self):
        ''' Get Sign In app '''
        if self._signInAppPage == None:
            self._signInAppPage = SignInAppPage(self)
        return self._signInAppPage

    @property
    def sign_in_app_pro_select(self):
        if self._signInAppPageProSelect == None:
            self._signInAppPageProSelect = SignInAppPageProSelect(self)
        return self._signInAppPageProSelect

    @property
    def home_app(self):
        ''' Get Home app '''
        if self._homeAppPage == None:
            self._homeAppPage = HomePageApp(self)
        return self._homeAppPage

    @property
    def home_app_pro_select(self):
        if self._homeAppPageProSelect == None:
            self._homeAppPageProSelect = HomePageAppProSelect(self)
        return self._homeAppPageProSelect

    @property
    def status_center_app(self):
        ''' Get Status Center app '''
        if self._statusCenterPage == None:
            self._statusCenterPage = StatusCenterApp(self)
        return self._statusCenterPage

    @property
    def fax_app(self):
        ''' Get Fax app '''
        if self._faxAppPage == None:
            self._faxAppPage = FaxAppPage(self)
        return self._faxAppPage

    @property
    def jobs_app(self):
        ''' Get Jobs app '''
        if self._jobsAppPage == None:
            self._jobsAppPage = JobsAppPage(self)
        return self._jobsAppPage

    @property
    def menu_page_app(self):
        ''' Get Menu app '''
        if self._menuApp == None:
            self._menuApp = MenuAppConstructor.construct(self)
        return self._menuApp

    @property
    def settings_page_app(self):
        ''' Get Settings app '''
        if self._settingsAppPage == None:
            self._settingsAppPage = SettingsAppPage(self)
        return self._settingsAppPage

    @property
    def tools_page_app(self):
        ''' Get Tools app'''
        if self._toolsAppPage == None:
            self._toolsAppPage = ToolsAppPage(self)
        return self._toolsAppPage

    @property
    def service_page_app(self):
        ''' Get Service app'''
        if self._serviceAppPage == None:
            self._serviceAppPage = ServiceAppPage(self)
        return self._serviceAppPage

    @property
    def universal_sign_in_app(self):
        ''' Get Wrapper for Signing In Regardless of Product'''
        if self._universalSignInAppWrapper == None:
            self._universalSignInAppWrapper = UniversalSignInWrapper(self)
        return self._universalSignInAppWrapper

    @property
    def quicksets_app(self):
        ''' Get Quicksets app'''
        if self._quicksetsApp == None:
            self._quicksetsApp = QuicksetsApp(self)
        return self._quicksetsApp

    @property
    def scan_to_email_app(self):
        ''' Get scan to email app'''
        if self._scanToEmailApp == None:
            self._scanToEmailApp = ScanToEmailApp(self)
        return self._scanToEmailApp

    def copy_page_app(self):
        ''' Get Copy app '''
        if self._copyApp == None:
            self._copyApp = CopyApp(self)
        return self._copyApp

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

    def wait_until_constrained(self, button, is_constrained=False):
        """
        Validates the constrained property of an object.
        """
        self.wait_until(lambda: button["constrained"] == is_constrained)

    def statusCenter_dashboard_expand(self):
        """
        Performs a mouse_click on status center dashboard
        to expand it when collapsed
        """
        logging.debug("UIType = " + str(self.uitype))
        if self.uitype == "Workflow2":
            pass #No Status Center in Workflow2
        if self.uitype == "Workflow":
            statusCenter = self.wait_for("NotificationCenterView")
            self.wait_until(lambda: statusCenter["visible"] == True)

            if statusCenter["state"] != "EXPANDED":
                statusCenterDash = self.wait_for("NotificationCenterView #footer #footerRectangle")
                logging.info(f"Need to Validate statusCenterDash={statusCenterDash} before mouse click")
                self.validate_button(statusCenterDash)
                statusCenterDash.mouse_click()
                time.sleep(3)

    def statusCenter_dashboard_collapse(self):
        """
        Performs a mouse_click on status center dashboard
        to collapse it when expanded
        """
        if self.uitype == "Workflow2":
            pass # No Status Center in Workflow2
        if self.uitype == "Workflow":
            statusCenter = self.wait_for("NotificationCenterView")
            state = statusCenter["state"]
            logging.debug(f"statusCenter_dashboard_collapse - 'state'={state}")
            if state != "COLLAPSED":
                statusCenterDash = self.wait_for("NotificationCenterView #footer #footerRectangle")
                logging.debug(f"statusCenter_dashboard_collapse - 'statusCenterDash'={statusCenterDash}")
                statusCenterDash.mouse_click()
                time.sleep(3)

    def get_alerts(self):
        device_alerts = []
        try:
            cdm_alerts = self.cdm.get(self.cdm.ALERTS)['alerts']
            logging.debug("Alerts Found : " + str(cdm_alerts))
            for alert in cdm_alerts:
                if 'actions' in alert:
                    device_alert = {"category": alert["category"]}
                    for action in alert['actions']:
                        if action == 'supported':
                            for value in alert['actions']['supported']:
                                device_alert['action'] = value['value']['seValue']
                        if action == 'links':
                            for action_link in alert['actions']['links']:
                                device_alert['href'] = action_link['href']
                    device_alerts.append(device_alert)
        except:
            pass
        return device_alerts

    def check_status_center_alert(self, alert_tittle):
        """
        Checks for an alert in status center
        Returns : True : Alert has been found.
                  False : Alert not Found.  
        """
        logging.info("Checking alert in Status Center ...")
        self.statusCenter_dashboard_expand()
        time.sleep(2)
        index, title = self._find_alert_title(alert_tittle)
        if title == None:
            self.statusCenter_dashboard_collapse()
            return False

        try:
            self.check_alert_icon("qrc:/images/Status/WarningFill.json", index)
        except (QmlItemNotFoundError, TimeoutError) as e:
            logging.info("Exception raised: " + str(e))
            self.statusCenter_dashboard_collapse()
            return False
        self.statusCenter_dashboard_collapse()
        return True

    def _find_alert_title(self , title):

        """
            Find alert given the expected title and return its index
            on status center along with the title
        """
        # alerts are added at the bottom, so let's scroll down in case the alert is hidden
        currentView = self.wait_for("NotificationView")
        currentView.mouse_wheel(0, -100)

        i = 0
        alertIndex = 0
        alertText  = ""
        found = False
        while not found:
            try : 
                alertTextQuery = self.query_item("#notificationRowAlertTitle #alertStatusCenterText", i)
                logging.info("alert title: " + str(alertTextQuery["text"]))
            except (QmlItemNotFoundError, TimeoutError) as e:
                logging.info("Exception raised: " + str(e))
                logging.info("Alert : {0} not Found")
                return None,None
            if str(alertTextQuery["text"]) == str(title):
                alertText = alertTextQuery["text"]
                found = True
            else:
                found = False
                i=i+1
                # apparently there can be empty rows, we have to discard them when looking for the alert's icon
                if str(alertTextQuery["text"]) != '':
                    alertIndex=alertIndex+1

        logging.info("alert index in status center" + str(alertIndex))

        return alertIndex, alertText

    def find_alert(self, title):
        """
        Finds an alert with the expected title and returns its index in the Status Center.
        If no matching alert is found, returns -1.
        """    
        alert_index = 0

        while True:
            # Alerts are added at the bottom, so let's scroll down in case the alert is hidden
            current_view = self.wait_for("NotificationView")
            current_view.mouse_wheel(0, -150)
            time.sleep(2)

            # Get the alert title
            try:
                alert_title = self.query_item("#notificationRowAlertTitle #alertStatusCenterText", alert_index)["text"]
                logging.info(f"Alert title: {alert_title}")
            except QmlItemNotFoundError:
                # If query_item fails, we have gone through all alerts
                break

            if alert_title == title:
                logging.info(f"Alert found in Status Center with index: {alert_index}")
                return alert_index
            else: 
                alert_index += 1

        logging.info(f"No alert with title '{title}' found in Status Center")
        return -1

    def check_alert_icon(self, icon, index):
        self.wait_for("#notificationRowIcon #mainImage")
        alertIcon = self.query_item("#notificationRowIcon #mainImage", index*2)
        assert str(alertIcon["source"]) == str(icon)

    def check_details_message(self, text):
        detailsMessage = self.wait_for("#alertDetailDescription  SpiceText[visible=true]")
        logging.info("detailsMessage = '{0}'".format(str(detailsMessage["text"])))
        assert str(detailsMessage["text"]) == str(text)

    def isWorkflowBase(self):
        return self.uitype == "Workflow" or self.uitype == "Workflow2"

    def _find_alert_in_alertApp_and_click(self , title):

        """
            Find alert given the expected title and click open it
        """
        alertButton = self.wait_for("#HomeScreenView #persistentHeader #headerVar2RightContainer #alertButton")
        self.wait_until(lambda: alertButton["visible"] == True)

        # click the alert button
        alertButton.mouse_click()
        self.wait_for("#alertAppView #alertAppHeader")
        index = 0
        found = False
        while not found:
            try:    
                alertStr = "#alertAppView #alert"+str(index)+" #alert"+str(index)+"_firstinfoBlockRow #contentItem"
                alertTextQuery = self.wait_for(alertStr)
                logging.info("alert title: " + str(alertTextQuery["text"]))
            except (QmlItemNotFoundError, TimeoutError) as e:
                logging.info("Exception raised: " + str(e))
                logging.info("Alert : {0} not Found")
                return None,None
            if str(alertTextQuery["text"]) == str(title):
                alertText = alertTextQuery["text"]
                # Click the alert with the title
                alertItem = self.wait_for("#alertAppView #alert"+str(index))
                alertItem.mouse_click()
                found = True
            else:
                found = False
                index = index+1

    def wait_button_status(self, button, expect_status):
        """
        Purpose: wait button status is same with expected.
        Args: button
              expect_status: True/False
        """
        start_time = time.time()
        end_time = start_time + QmlTestServer.WAIT_TIMEOUT
        while time.time() < end_time:
            button_status = button["enabled"]
            logging.info(f"button status is: {button_status}, expect status is: {expect_status}")
            if button_status == expect_status:
                logging.info(f"Already wait button expect status: {expect_status}")
                break
        else:
            raise Exception(f"Not wait expected button state: {expect_status} in {QmlTestServer.WAIT_TIMEOUT} seconds.")

    def dismiss_keyboard(self):
        """
        Attempts to dismiss any visible keyboard by clicking appropriate dismiss buttons.
        Returns True if keyboard was found and dismissed, False otherwise.
        """
        try:
            keyboard_view = self.wait_for("#spiceKeyboardView", timeout=2)
            if keyboard_view["visible"]:
                try:
                    hide_key_numeric_keyboard = self.query_item("#keyboard #hideKeyboardKeyPositiveIntegerKeypad")
                    hide_key_numeric_keyboard.mouse_click()
                    return True
                except:
                    try:
                        hide_key = self.query_item("#hideKeyboardKey")
                        hide_key.mouse_click()
                        return True
                    except:
                        logging.debug("Could not find keyboard dismiss buttons")
                        return False
        except:
            logging.debug("No keyboard view visible")
            return False
        return False
