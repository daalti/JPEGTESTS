
class Locators:
    # Views
    settings_app_view = "#settingsMenuListListView"

    # Buttons
    home_button = settings_app_view + " " + settings_app_view + "list1 #menuListListViewHeader #BreadcrumbView #HomeButton #ButtonControl"
    general_tab_button = settings_app_view + "list1 #generalSettingsSettingsTextImage #mouseArea"
    date_and_time_button = settings_app_view + " #GenericStructureView #panelsStack #generalSettingsMenuList #dateTimeWFSettingsTextImage #mouseArea"
    time_zone_tab_button = settings_app_view + " #dateTimeSettingView #timeZoneSettingsTextImageBranch #mouseArea"
    display_button = settings_app_view + " #displaySettingsTextImage #mouseArea"

    # Combo Boxes
    inactivity_timeout_combo_box = "#inactivityTimeoutWFMenuComboBox"

    # Scroll Bars
    inactivity_timeout_combo_box_scroll_bar = "#comboBoxScrollBar"
    display_tab_scroll_bar = "#displayMenuListScrollBar"

    # Pop Up List
    inactivity_timeout_pop_up_list = "#SettingsSpiceComboBoxpopupList"