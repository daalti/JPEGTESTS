
import sys

class IWorkflowUICommonOperations(object):

    def back_button_press(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_item(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_help_content(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_sub_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_settings_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def goto_network_settings_menu(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def verify_jam_autonav_ui_alert(self, net, stringID, stepID, installed_Trays, btn_click, locale: str = "en-US"):
        """
        Verify the alert message for Jam AutoNav UI
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def checkingAlertMessageStrings(self,net,alertStringIdsArray,locale:str = "en-US"):
        """
        verify the message content of the alert message.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
    
    def check_and_click_radioButton(self, radioButtonId, title, clickable=False):
        """
        Check and click the radio button
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
        
    def scroll_item_into_view(self, comboboxpopuplist, scroll_bar, list_item):
        """
        This scroll function is special case for ComboBoxpopupList. And scroll item into view then it can be selected.
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def scroll_screen_via_height(self, screenid, sroll_height, time_delay=2):
        """
        Scroll screen via height, then could go through item one by one with limited max contentY to avoid last item displayed in center of screen  
        Especially for last item, cannot operation the last item normally in part screen when it is in screen center via function scroll_bar["position"] to set value position, actually this item 
        should display at the bottom of screen. At this time, this item will be reset to bottom location rather then clicked/checked box selected

        screen id: the parent screen of row item, this screen should contain property "contentHeight"/"contentY"/"height"
        sroll_height: the heght of row item
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def validate_list_object_is_in_vertical_screen_view(self, screen_id, menu_item_id, footer_item_id=None, top_item_id=None):
        """
        To check the item is in screen view then it can be click, need to conside Begining Y of screen
        -> one secnario is less then 0, such -60
        -> one secnario is 0, such as 0
        Also need to conside footer object when it is included in scroll screen view
        screen_id:
        menu_item_id:
        footer_item_id
        """
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
