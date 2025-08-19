import sys


class IHomeAppUIOperations(object):

   def goto_home_menu(self):
      raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

   def goto_home_copy(self):
      raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

   def get_all_button_ids(self):
      raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

   def goto_home_fax(self):
      raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

   def goto_home_fax_configured_faxsendrecipient_screen(self):
      raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

   def fax_menu_navigation(self, button_object_id, expected_object_id, select_option: bool = True):
      raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
   
   def is_back_button_visible(self):
      raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

   def is_cancel_button_visible(self):
      raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
