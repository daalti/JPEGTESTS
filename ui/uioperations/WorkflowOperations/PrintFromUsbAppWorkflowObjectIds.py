class PrintFromUsbAppWorkflowObjectIds:

    """
    Print from USB app objects ids add under this class
    """
    # VIEWS/SCREENS
    home_screen_view = "#HomeScreenView"
    print_app = "#02FECD9A-7FE7-4797-AD15-8127DF2CFAADMenuApp"
    print_from_usb = "#c93bc831-99a8-454c-b508-236fc3a2a08f"
    job_storage = "#HomeFolderView #86DCD04A-5F44-4EAE-83C3-1C3C3F12E32B MouseArea"
    quick_forms_app = "#6c8ddc45-4b4d-44cb-b5c9-f48a0574fe42"
    icon_print_from_usb = "#c93bc831-99a8-454c-b508-236fc3a2a08fMenuApp"
    view_print_from_usb_landing = "#02FECD9A-7FE7-4797-AD15-8127DF2CFAADMenuAppList" #TBD
    scrollBar_printFolderPage = "#02FECD9A-7FE7-4797-AD15-8127DF2CFAADMenuAppListScrollBar"
    printFolderPage_column_name = "#02FECD9A-7FE7-4797-AD15-8127DF2CFAADMenuAppListcolumn"
    printFolderPage_Content_Item = "#02FECD9A-7FE7-4797-AD15-8127DF2CFAADMenuAppListlistItem"

    usb_defect_header_str_id = "cInsertUsbDeviceTitle"
    usb_defect_header = "#noUSB"
    usb_cancel_button_str_id = "cCancel"
    usb_cancel_button = "#noUSBCancelBtn"

    usb_disconnected_button = "#disconnectedUSBOkBtn"

    usb_no_file_str_id = "cUnableToFindFilesFolders"
    usb_defect_locator = "#noFileFoundColumn"
    usb_ok_button_str_id = "cOKButton"
    print_usb_no_content_ok_button = "#noFileFoundUsbOkBtn"
    print_from_usb_button_locator = "#c93bc831-99a8-454c-b508-236fc3a2a08fMenuApp"

    print_usb_folder_landing_view = "#printUsbFolderLandingView"
    print_usb_folder_list_view = "#printUsbFolderListView"
    print_usb_folder_grid_view = "#printUsbFolderGridView"
    print_usb_folder_more_options_button = "#printUsbFolderLandingViewMoreOptions"
    print_usb_folder_header_view_folder_title_locator = "#SpiceBreadcrumb #BreadcrumbView #textContainer SpiceText[visible=true]"

    print_usb_app_view = "#PrintUsbAppApplicationStackView"
    view_print_usb_folder_list_view = "#SpiceListViewView"
    view_print_usb_folder_grid_view = "#scrollAreaGridLayout"
    print_usb_folder_list_view_scroll = "#SpiceListViewViewScrollBar"  
    print_usb_folder_grid_view_verticalscroll = "#scrollAreaGridLayoutverticalScroll"  
    
    header_print_from_usb_str_id = "cRetrieveFromUSB"
    print_button_str_id = "cPrint"
    continue_button_str_id = "cContinue"
    print_button_locator = "#printUsbBtn"
    continue_button_locator = "#continueButton"
    print_cancel_job_button_locator = "#cancelUsbJobBtn"
    print_cancel_button_locator = "#cancelButton"
    print_cancel_confirm_button_locator = "#cancelJobButton"
    footer_detail_print_button_locator = "#printUsbBtnFD"
    job_status_scrollbar = "#jobQueueJobListScrollBar"
    back_button = "#BackButton"
    print_cancel_job_button_footer_locator = "#cancelUsbJobBtnFD"

    # preview
    print_usb_folder_preview_button = "#previewButton"
    preview_screen_for_small = "#fitpagePreviewForPrintJob"
    preview_screen_for_large = "#PREVIEW_FLICABLE_CONTENT_AREA"
    preview_screen_progress = "#PREVIEW_IMAGE"
    preview_screen_header = "#previewHeader"
    preview_screen_header_moreOptions = "#moreOptions"
    preview_screen_header_backButton = "#previewHeader #BackButton"
	
    # no of copies
    numberOfCopies_locator = "#printFromUSB_numberOfCopiesMenuSpinBox"
    numberOfCopies_plus_locator = "#upBtn"
    numberOfCopies_minus_locator = "#downBtn"
    numberOfCopies_textArea_locator = "#SpinBoxTextInput"
	
    # option 
    options_view = "#printSelectSettingsViewlist1"
    options_view_scrollbar = "#printSelectSettingsViewlist1ScrollBar"
    options_two_sided_setting_switch = "#printFromUSB_twoSidedSettingsSwitch"
    options_two_sided_menu_switch = "#printFromUSB_twoSidedMenuSwitch" 

    #sides option
    option_sides_str_id = "cSides"
    option_two_sided_menu_loctor = "#printFromUSB_twoSidedSettingsComboBox"
    option_two_sided_button_locator = "#printFromUSB_twoSidedComboBox"
    option_two_sided_set_simplex = "#ComboBoxOptionssimplex"
    option_two_sided_set_duplex = "#ComboBoxOptionsduplex"

    property_checked = "checked"
    property_selected = "selected"
    option_button_close = "#closeButton"

    # quality_options
    option_quality_menu_loctor = "#printFromUSB_qualitySettingsComboBox"
    quality_quality_str_id = "cQuality"
    option_quality_button_locator = "#printFromUSB_qualityComboBox"
    option_quality_set_normal = "#ComboBoxOptionsnormal"
    option_quality_set_best = "#ComboBoxOptionsbest"
    option_quality_set_draft = "#ComboBoxOptionsdraft"

    # paper source (jupiter, beam)
    option_paper_source_menu_loctor = "#printFromUSB_paperSourceSettingsComboBox"
    option_paper_source_button_locator = "#printFromUSB_paperSourceComboBox"


    # color option
    color_color_str_id = "cColorMode"
    option_color_menu_loctor = "#printFromUSB_colorSettingsComboBox"
    option_color_button_locator = "#printFromUSB_colorComboBox"
    option_color_set_color = "#ComboBoxOptionscolor"
    option_color_set_grayscale = "#ComboBoxOptionsgrayscale"
    option_color_set_auto = "#ComboBoxOptionsautoDetect"
    option_color_set_grayscale_xl = "#ComboBoxOptionsgrayscale"

	# collate option
    options_collate_menu_switch = "#printFromUSB_collateMenuSwitch"
    options_collate_setting_switch = "#printFromUSB_collateSettingsSwitch"

    # page order option
    options_page_order_menu_locator = "#printFromUSB_printingOrderSettingsComboBox"
    options_page_order_button_locator = "#printFromUSB_printingOrderComboBox"
    option_first_page_on_top = "#ComboBoxOptionsfirstPageOnTop"
    option_last_page_on_top = "#ComboBoxOptionslastPageOnTop"

    # rotation option
    options_rotation_menu_locator = "#printFromUSB_rotationSettingsComboBox"
    options_rotation_button_locator = "#printFromUSB_rotationComboBox"
    option_rotation_auto = "#ComboBoxOptionsauto_"
    option_rotation_0_degrees = "#ComboBoxOptionsrotate0"
    option_rotation_90_degrees = "#ComboBoxOptionsrotate90"
    option_rotation_180_degrees = "#ComboBoxOptionsrotate180"
    option_rotation_270_degrees = "#ComboBoxOptionsrotate270"

    # paper selection
    paperSelection_str_id = "cPaperSelectTitle"
    option_paperSelection_menu_loctor = "#printPaperSelectionView"
    option_paperSelection_menu_list = "#printFromUSB_paperSelectionMenuList"
    paper_selection_settings_view = "#printPaperSelectionView"
    option_paperTray_menu_locator = "#printFromUSB_paperTraySettingsTextImage"
    option_paperTray_menu_comboBox = "#printFromUSB_paperTrayIComboBox"
    option_paperSelection_value = "#printPaperSelectionView_2infoBlockRow"
    
    detail_panel_layout = "#DetailPanelverticalLayout"
    options_button_locator = "#printModeBtn"
    expand_button_locator = "#_ExpandButton"
    collapse_button_locator = "#_CollapseButton"
    close_print_mode_button_locator = "#closeButton"
    print_settings_view = "#printUsbFolderLandingView"
    detail_panel_layout_scrollbar = "#DetailPanelverticalLayoutScrollBar"

    toast_message_text = "#infoTextToastMessage"
	
    view_optionView = "#printSelectSettingsViewlist1"
    view_option_paperSelection = "#printFromUSB_paperSelectionMenuList"
    view_printSettings_paperTray = "#printFromUSB_paperTraySettingsTextImage_2infoBlockRow"

    # paper size
    option_paperSize_menu_locator = "#printFromUSB_paperSizeSettingsTextImage"
    view_option_paperSelection_paperSize = "#printFromUSB_paperSizeMenuSelectionList"
    paper_size_list_view_scroll_bar = "#printFromUSB_paperSizeMenuSelectionListScrollBar"
    radio_paperSize_iso_a4_210x297mm = "#MenuValueiso_a4_210x297mm"
    paper_size_item_radio_button = "#SpiceRadioButton"
    view_printSettings_paperSize = "#printFromUSB_paperSizeSettingsTextImage_2infoBlockRow"

    # paper type
    option_paperType_menu_locator = "#printFromUSB_paperTypeSettingsTextImage"
    view_option_paperSelection_paperType = "#printFromUSB_paperTypeMenuSelectionList"
    paper_type_list_view_scroll_bar = "#printFromUSB_paperTypeMenuSelectionListScrollBar"
    paper_type_item_radio_button = "#SpiceRadioButton"
    view_printSettings_paperType = "#printFromUSB_paperTypeSettingsTextImage_2infoBlockRow"
    paper_type_UserType10 = "#MenuValuecom_dot_hp_dot_usertype_dash_10"

 
    # print_margins_options
    option_print_margins_menu_loctor = "#printFromUSB_marginSettingsComboBox"
    print_margins_str_id = "cPrintMargins"
    option_print_margins_button_locator = "#printFromUSB_marginComboBox"
    option_print_margins_set_clip_from_contents = "#ComboBoxOptionsclipContents"
    option_print_margins_set_add_to_contents = "#ComboBoxOptionsaddToContents"
    option_print_margins_set_oversize = "#ComboBoxOptionsoversize"
    
    # defaultOutputDestination
    option_print_defaultOutputDestination_menu_locator = "#printFromUSB_defaultOutputDestinationSettingsComboBox"
    print_defaultOutputDestination_str_id = "cDefaultOutputDestination"
    option_print_defaultOutputDestination_button_locator = "#printFromUSB_defaultOutputDestinationComboBox"
    option_print_defaultOutputDestination_set_stacker = "#ComboBoxOptionsstacker_dash_1"
    option_print_defaultOutputDestination_set_folder = "#ComboBoxOptionsfolder_dash_1"
    #defaultFoldingStyleComboBox
    option_print_defaultFoldingStyle_button_locator = "#printFromUSB_defaultFoldingStyleComboBox"

    # output_scale_options
    option_output_scale_menu_loctor = "#printUsbSettingResize"
    option_output_scale_view= "#printUsbResizeView"
    output_scale_str_id = "cOutputScale"
    option_output_scale_button_locator = "#printUsbSettingResize_2infoBlockRow"
    option_output_scale_set_none = "#none"
    option_output_scale_set_custom = "#customRadioButton"
    option_output_scale_set_custom_spin_box = "#customSpinBox"
    option_output_scale_set_custom_spin_box_plus_locator = "#upBtn"
    option_output_scale_set_custom_spin_box_minus_locator = "#downBtn"
    option_output_scale_set_loaded_paper = "#scaleToOutputRowRadioButton"
    option_output_scale_set_loaded_paper_detail = "#scaleToOutputRowComboBox"
    option_output_scale_set_loaded_paper_detail_roll1 = "#roll_dash_1"
    option_output_scale_set_loaded_paper_detail_roll2 = "#roll_dash_2"
    option_output_scale_set_loaded_paper_detail_tray = "#main"

    option_output_scale_set_standard_sizes = "#standardSizeScalingRowRadioButton"
    option_output_scale_set_standard_sizes_detail = "#standardSizeScalingRowComboBox"
    option_output_scale_set_standard_sizes_detail_a0 = "#iso_a0_841x1189mm"
    option_output_scale_set_standard_sizes_detail_a1 = "#iso_a1_594x841mm"
    option_output_scale_set_standard_sizes_detail_a2 = "#iso_a2_420x594mm"
    option_output_scale_set_standard_sizes_detail_a3 = "#iso_a3_297x420mm"
    option_output_scale_set_standard_sizes_detail_a4 = "#iso_a4_210x297mm"
    option_output_scale_set_standard_sizes_detail_b1 = "#iso_b1_707x1000mm"
    option_output_scale_set_standard_sizes_detail_b2 = "#iso_b2_500x707mm"
    option_output_scale_set_standard_sizes_detail_b3 = "#iso_b3_353x500mm"
    option_output_scale_set_standard_sizes_detail_b4 = "#iso_b4_250x353mm"
    option_output_scale_set_standard_sizes_detail_letter = "#na_letter_8_dot_5x11in"
    option_output_scale_set_standard_sizes_detail_ledger = "#na_ledger_11x17in"
    option_output_scale_set_standard_sizes_detail_ansi_c = "#na_c_17x22in"
    option_output_scale_set_standard_sizes_detail_ansi_d = "#na_d_22x34in"
    option_output_scale_set_standard_sizes_detail_ansi_e = "#na_e_34x44in"
    option_output_scale_set_standard_sizes_detail_arch_a = "#na_arch_dash_a_9x12in"
    option_output_scale_set_standard_sizes_detail_arch_b = "#na_arch_dash_b_12x18in"
    option_output_scale_set_standard_sizes_detail_arch_c = "#na_arch_dash_c_18x24in"
    option_output_scale_set_standard_sizes_detail_arch_d = "#na_arch_dash_d_24x36in"
    option_output_scale_set_standard_sizes_detail_arch_e = "#na_arch_dash_e_36x48in"
    standard_sizes_optionView = "#standardSizeScalingRowComboBoxpopupList"
    standard_sizes_scrollbar = "#comboBoxScrollBar"

    #cartridge very low
    cartridge_very_low_str_id = "cCartridgesVeryLow"
    cartridge_very_low_locator = "#titleObject"

    view_load_paper_error_view = "#mediaLoadFlowWindow"
    ok_button_load_paper_error_view = "#mediaLoadFlowWindow #OK"
    cancel_button_load_paper_error_view = "#cancelButton"

    view_media_mismatch_type = "#mediaMismatchTypeFlowWindow"
    ok_button_media_mismatch_type = "#mediaMismatchTypeFlowWindow #OK"

    view_media_mismatch_size = "#mediaMismatchSizeFlowWindow"
    ok_button_media_mismatch_size = "#mediaMismatchSizeFlowWindow #OK"
    ok_button_media_mismatch_size_for_mm = "#mediaMismatchSizeFlow #Print"
    view_print_usb_search_view = "#printUSBSearchView"
    option_sort =   "#customSectionOptions #sortButton"
    option_filter = "#customSectionOptions #filterButton"
    option_search = "#customSectionOptions #searchButton"

    view_confirm_loaded_paper = "#alertModalView"
    ok_button_confirm_loaded_paper = "#alertModalView #OK"

    reading_usb_progress_locator = "#readingProgress"

    search_text_field_locator = "#searchTextField"
    ok_button_keyboard = "#enterKey1"
    search_button_locator = "#rowLayoutForSearch #arrowBtn"
    search_result_message_locator = "#searchResult SpiceText[visible=true]"
    button_on_search_screen = "#rowLayoutForSearch #ButtonControl"
    text_view_constraint_message = "#ConstraintMessage #constraintDescription #contentItem"
    search_file_folder_str_id = "cSearchFileFolderName"

    filter_list_view = "#filterList"
    filter_list_view_scroll_bar = "#filterListScrollBar"
    filter_option_jpeg = "#JPEG"
    filter_option_all_file_type = "#AllFileTypes"
    filter_option_ps = "#PS"
    filter_option_tiff = "#TIFF"
    filter_option_pdf = "#PDF"
    filter_option_ppt = "#PPT"
    filter_option_doc = "#DOC"

    save_button_filter_screen = "#printUsbFilterSave"

    sort_option_a_to_z = "#AtoZ"
    sort_option_z_to_a = "#ZtoA"
    sort_option_old_to_new = "#OldToNew"
    sort_option_new_to_old = "#NewToOld"
    sort_option_scrollbar = "#printUsbSortView #sortListScrollBar"

    save_button_sort_screen = "#printUsbSortSave"

    view_constraint_message = "#ConstraintMessage"
    ok_button_constrained_message = "#okButton"
    view_constraint_message_str_id = "cOperationNotAllowed"
    view_constraint_message_content = "#constraintDescription"

    # Preview screen
    file_preview_button = "#{0} #previewButton"
    preview_template = "#previewTemplate"
    preview_title = "#previewTemplate #HeaderViewLeft #textContainer SpiceText[visible=true]"
    preview_back_button = "#previewTemplate #BackButton"
    
    # Pagination
    scroll_area_grid_layout = "#scrollAreaGridLayout"
    scroll_area_grid_layout_vertical_layout = "#scrollAreaGridLayout #scrollAreaGridLayoutverticalScroll"
    print_usb_folder_grid_view = "#printUsbFolderGridView"
    button_last_page = "#rightLastButton"
    button_next_page = "#rightButton"
    page_indicator = "#pageIndicator"
    page_indicator_loader = "#pageIndicatorLoader"
    page_indicator_mouse_area = "#pageIndicatorMouseArea"
    frist_page_indicator_mouse_area = "#pageIndicatorMouseArea0"
    button_previous_page = "#leftButton"
    button_first_page = "#leftFirstButton"