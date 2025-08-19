class Locators:
    # VIEWS

    ui_copy_app = "#copyLandingView"
    copy_settings_view = "#copySettingsView"    

    # BUTTONS
    # mainActionButtonOfDetailPanel is repeated because the main button has different uses.
    # but it has different variables here so we know in the tests what string and button type
    # is expected to appear on the UI
    copy_button = "#mainActionButtonOfDetailPanel"
    done_button = "#mainActionButtonOfDetailPanel"
    eject_button = "#ejectMainPanelButton"

    copy_button_expanded = "#mainActionButtonOfMainPanel"
    done_button_expanded = "#mainActionButtonOfMainPanel"

    # STRINGS  
    number_of_copies = "#copy_numberOfCopiesMenuSpinBox"
    paper_source_combo = "#copy_detailedPaperSourceComboBox"
    paper_source_combo_popup = "#copy_detailedPaperSourceComboBoxpopupList"
    property_text_button = "SpiceText[visible=true]"
    copy_string_id_button = "cCopy"
    done_string_id_button = "cDoneButton"
    start_string_id_button = "cStart"

    # FOOTER BUTTONS
    options_detail_panel_button = "#optionsDetailPanelButton"
    close_copy_settings_button = "#closeButton"
    home_button_clickable = "#HomeButton #ButtonControl"

