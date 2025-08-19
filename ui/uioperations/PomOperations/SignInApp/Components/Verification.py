from ..Page import Page

class Verification():
    def __init__(self, page:Page) -> None:
        self.__page = page

    def verify(self, expected_view_locator:str, verify_active_focus:bool = True, timeout = Page.DEFAULT_TIMEOUT) -> bool:
        element = self.__page.wait_for_element(expected_view_locator, timeout=timeout)
        if element == None: return False
        if verify_active_focus == False: return True
        return self.__page.check_element(element, self.__page.Attribute.ActiveFocus, True, timeout)