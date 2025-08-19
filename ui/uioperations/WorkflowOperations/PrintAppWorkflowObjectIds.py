class PrintAppWorkflowObjectIds:
    """
    It contains print app object IDs of workflows ui
    """
    #cleaning pages
    cleaning_pages_combobox_scroll_bar = "#comboBoxScrollBar"
    cleaning_pages_combobox_screen = "#SettingsSpiceComboBoxpopupList"
    cleaning_pages_settings_dic = {
        "1000_pages" : "#1000Button",
        "2000_pages" : "#2000Button",
        "5000_pages" : "#5000Button",
        "10000_pages" : "#10000Button",
        "20000_pages" : "#20000Button",
        "off" : "#StringIds.cOffButton",
    }
    clean_smear = "#cleanSmear"
    view_clean_smear = "#inputsSelectionScreen"
    clean_smear_continue_button = "#continueButton"
    view_progress_screen = "#calibrationDelayProgress"
    view_print_head_cleaning = "#multiCalibrationHeaderHeaderView"
    print_head_cleaning_level2 = "#hardCleanPh"
    print_head_cleaning_level3 = "#cleanPhLevel3"
    #print quilty speed settings
    quality_speed_settings = "#qualityComboBox"
    quality_speed_dict = {
        "draft": "#ComboBoxOptionsdraft",
        "normal": "#ComboBoxOptionsnormal",
        "best": "#ComboBoxOptionsbest"
    }
    view_quality_combobox = "#qualityComboBoxpopupList"
    #print sides settings
    sides_dict = {
        "1-sided": "#ComboBoxOptionssimplex",
        "2-sided": "#ComboBoxOptionsduplex"
    }
    row_object_sides = "#sidesWFSettingsComboBox"
    view_combo_box_sides = "#sidesWFComboBoxpopupList"
    view_printquality_screen = "#PrintQualityScroller"
    
    #powerOnCalibration
    power_on_calibration = "#colorCalibrationPowerOnConfiguration #SettingsSpiceComboBox"
    power_on_calibration_options = "#SettingsSpiceComboBoxpopupList"
    power_on_calibration_scroller = '#comboBoxScrollBar'
    power_on_calibration_Immediate  = "#powerOnOptionImmediate"
    power_on_calibration_5minutes   = "#powerOnOption5Minutes"
    power_on_calibration_15minutes  = "#powerOnOption15Minutes"
    power_on_calibration_30minutes  = "#powerOnOption30Minutes"
    power_on_calibration_60minutes  = "#powerOnOption60Minutes"

    clean_belt = "#CleanBelt"

    #envelope rotate
    envelope_rotate_menu = "#envelopeRotateSelectionMenuComboBox"
    envelope_rotate_settings = "#envelopeRotateSelectionMenuComboBox #SettingsSpiceComboBox"    
    envelope_rotate_options = "#SettingsSpiceComboBoxpopupList" 