
import sys

class IWorkflowKeyboardUICommonOperations(object):

    def keyboard_press_icon(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_enter_character(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_enter_text(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_set_text_with_out_dial_action(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_enter_number(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)

    def keyboard_clear_text(self):
        raise NotImplementedError('Unimplemented method %s' % sys._getframe().f_code.co_name)
