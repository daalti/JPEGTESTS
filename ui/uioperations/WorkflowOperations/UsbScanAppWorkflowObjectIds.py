class UsbScanAppWorkflowObjectIds:
    """
        Usb Scan app objects ids add under this class
    """

    # VIEWS/SCREENS
    view_scan_usb_landing = "#scanUsbLandingView"
    view_usb_folder = "#usbSelectFolderView"
    folder_list_screen_view = "#folderList"
    view_usb_unsupported_device_error = "#usbUnsupportedDeviceError"
    menu_list_scan_settings = "#scanMenuList"
    view_quickset_app_landing = "#quickSetsLandingPageView"
    create_folder_screen_view = "#createFolderView"
    information_message = "#informationMessage"
    error_message = "#errorMessage"
    all_option_view = "#scanMenuListlist1"

    # WIDGETS ON SCREEN : Buttons,text boxes,menu icons etc..
    icon_scan_usb_drive = "#df4a8a01-7659-486f-95d5-e125ccd1529aMenuApp"
    usb_drive_app = "#USBFolderGUID"
    view_scan_screen = "#D1AC8C3A-9503-44f8-AFD8-9FAC389F6E32MenuAppList"
    scrollBar_menuscanFolderLanding = "#D1AC8C3A-9503-44f8-AFD8-9FAC389F6E32MenuAppListScrollBar"
    scanFolderPage_column_name = "#D1AC8C3A-9503-44f8-AFD8-9FAC389F6E32MenuAppListcolumn"
    scanFolderPage_Content_Item = "#D1AC8C3A-9503-44f8-AFD8-9FAC389F6E32MenuAppListlistItem"
    button_scan_usb_home_edit = "#ButtonControl"
    scan_usb_selected_Directory = "#selectedDirectory"
    button_scan_usb = "#df4a8a01-7659-486f-95d5-e125ccd1529a"
    scan_usb_app_button = button_scan_usb+" MouseArea"

    # Buttons
    button_usb_options = "#FooterViewRight #optionsButton"
    eject_button = "#ejectButtonMainLeftBlock"
    collapse_button = "#_CollapseButton"
    button_close_options = "#closeButton"
    edit_button = "#scanUsbLandingView #usbScanFolderSettings #ButtonControl"

    # Pagination
    page_indicator_view = "#SpicePageIndicator #SpicePageIndicatorView"
    button_last_page = "#rightLastButton"
    button_next_page = "#rightButton"
    page_indicator = "#pageIndicator"
    page_indicator_mouse_area = "#pageIndicatorMouseArea"
    frist_page_indicator_mouse_area = "#pageIndicatorMouseArea0"
    button_previous_page = "#leftButton"
    button_first_page = "#leftFirstButton"
    folder_grid_item = "#folderGridItem"
    usb_select_folder_footer = "#usbSelectFolderFooter"
    usb_select_folder_layout = "#bodyLayoutverticalLayout"
    usb_select_folder_scroll_bar = "#bodyLayoutverticalLayoutScrollBar"

    #Common buttons
    button_home = "#HomeButton"
    button_back = "#BackButton"
    button_usb_save_here_button = "#saveButton"
    button_scan_usb_landing_cancel = "#cancelButton"
    button_usb_send = "#sendButtonDetailRightBlock"
    button_usb_start = "#startButtonDetailRightBlock"
    button_usb_done = "#doneButtonDetailRightBlock"
    button_usb_preview = "#previewButtonDetailRightBlock"
    button_usb_stop_scan = "#stopScanButtonDetailRightBlock"
    view_usb_scan_progress = "#SystemProgressView"  # To do:dummy object id
    button_usb_scan_progress_cancel = "#cancelJobButton"
    button_usb_create_folder = "#createfolderButton"

    view_scan_usb_no_front_device = "#ConstraintMessage"
    button_scan_usb_no_front_device_cancel = "#okButton"
    view_usb_scan_save_success = "#saveSuccessfulView"  # To do:dummy object id
    button_usb_scan = "#UsbScanButton"  # To do:dummy object id
    view_usb_scan_details = "#usbDetailsView"  # To do:dummy object id
    button_usb_scan_filename = "#fileNameTextField"
    scan_usb_file_name_input = "#TextInputBox"
    view_common_keyboard = "#spiceKeyboardView"
    button_usb_scan_filetype = "#UsbFileTypeButton"  # To do:dummy object id
    scan_usb_file_name_read_only_view = "#ConstraintMessage"
    scan_usb_file_name_read_only_ok_button = "#okButton"
    scan_usb_folder_name_input = "#folderNameTextInputBox"
    button_usb_folder_add = "#folderAdd"
    button_usb_folder_add_cancel = "#folderNameCancel"
    button_folder_name_already_exist_ok = "#folderNameAlreadyExistOkBtn"
    ok_button_message = "#okButton"
    hide_button = "#hideScanJam"
    paper_jam_window = "#jamInScannerWindow"
    paper_jam_alert_description = "#alertDetailDescription"
    view_constraint_message = "#ConstraintMessage"
    constrain_description_view = "#constraintDescription"
    scan_usb_folder_name_input_error_massage = "#textFieldContainer #HelperMessageContentItem #HelperText"

    ##scrollbar
    screen_id = "#DetailPanelverticalLayout"
    scrollbar_usb_landing_page = "#DetailPanelverticalLayoutScrollBar"
    row_object_usb_insert = "#usbScanFolderSettings"
    button_keyboard_ok = "#enterKey1"

    row_object_filename = "#scanFileNameFieldDestination"
    quickset_selection_view = "#qsScroll"
    quickset_selection_view_horizontal_bar = "#qsScrollhorizontalScroll"
    scrollbar_all_option = "#scanMenuListlist1ScrollBar"
    default_quickset_button = "#Default"
    view_all_locator = "#ViewAll"
    defaults_and_quick_sets_view = "#SpiceListViewView"
    quick_sets_view = "#QSListofApp"
    save_as_default_button = "#savePanelButton"
    text_column_of_detail = "#LayoutHorizontalIconsGrid"
    contentItem = "#contentItem"
    text_title = "#TitleText"
    button_ok = "#OKButton"
    usb_disconnect_ok_button = "#AlertFooter #okButton"

    file_format_comboBox = "#scan_fileFormatSettingsComboBox #scan_fileFormatComboBox"
    file_format_comboBox_option = "#ComboBoxOptions{}"

    view_menu_save_options = "#SaveOptionsForQSlist1"
    usb_quickset_as_defaults_option = "#AsDefaults"
    ok_under_save_option_veiw = "#saveoptionOK"
    cancel_under_save_option_veiw = "#saveoptionCancel"
    save_as_default_alert_view = "#Layout2ColumnsNrowsGrid"
    save_as_default_alert_save_button = "#messageSave"
    combobox_close_button = "#closeButton"
    menu_list_scan_settings_close_button = "#closeButton"
    view_scan_job_toastwindow = "#ToastWindowToastStackView"
    destination_name = "#usbScanFolderSettings #SpiceNameValue #ValueText"

    #usbFoldersScrollBar    
    view_usb_folders_scrollbar = "#bodyLayoutverticalLayoutScrollBar"

    clear_text_filename = "#ClearMouseArea"

    #Properties
    property_text_button = "SpiceText[visible=true]"
    
    notify_only_when_job_fail_option_view_model = "#notifyOnlyOnFailRBViewModel"
    notify_after_job_finishes_option_view_model = "#notifyAfterJobFinishesRBViewModel"
    do_not_notify_option_view_model = "#doNotNotifyRBViewModel"
    include_thumbnail_check_option_view_model = "#includeThumbnailCheckBoxViewModel"
    notify_only_when_job_fail_option_control_model = "#notifyOnlyOnFailRBControlModel"
    notify_after_job_finishes_option_control_model = "#notifyAfterJobFinishesRBControlModel"
    do_not_notify_option_control_model = "#doNotNotifyRBControlModel"
    include_thumbnail_check_option_control_model = "#includeThumbnailCheckBoxControlModel"
    scan_job_notification_done_button = "#sendJobNotificationDoneButton"