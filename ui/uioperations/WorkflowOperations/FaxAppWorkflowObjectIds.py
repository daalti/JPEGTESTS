from enum import Enum
from dunetuf.fax.fax import FaxModemType

class FaxAppWorkflowObjectIds:

    # VIEWS/SCREENS
    fax_receive_fax_printing_options = "#FaxPrintingValue_2infoBlockRow"
    fax_receive_setting_fax_printing_options_screen = "FaxPrinting"
    fax_printing_option_screen_alwaysprint_radiobutton = "#alwaysPrint"
    fax_printing_option_screen_alwaysstore_radiobutton = "#alwaysStore"
    fax_printing_option_screen_alwaysstoreandprint_radiobutton = "alwaysStoreAndPrint"
    fax_printing_option_screen_hintTextRow = "#hintTextRow"
    fax_printing_option_screen_hintText = "#hintTextTitle"
    fax_receive_setting_fax_printing_option_screen="#faxPrintingComboBoxpopupList"
    fax_receive_fax_printing_setting_combox = "#faxPrintingSettingsComboBox"
    fax_receive_setting_fax_printing_option="#FaxPrintingValue"
    fax_receive_setting_fax_printing_always_print="#alwaysPrint"
    fax_receive_setting_fax_printing_store_and_print="#alwaysStoreAndPrint"
    combo_box_fax_printing="#faxPrintingComboBox"
    fax_app_home = "#44aa632b-cfa3-4c10-8cab-697a9bef610b"
    fax_setup_countryopt ="#countryList"
    view_optionsScreen = "#faxSettingsPageMenuListListViewlist1"
    view_faxSettingsScreen = "#faxSettingsMenuList"
    view_faxSendSettingsScreen =  "#faxSendMenuList"  
    view_faxDialingScreen = "#faxDialingMenuList"
    view_DualfaxDialingScreen = "#faxDialingDualLineMenuList"
    view_distinctiveRingScreen = "#faxSetupDistinctiveRingTypeView"  # Need to be replaced later
    
    restricted_access_alert_message = "#noAccessView"
    restricted_access_alert_message_ok_button = "#noAccessOkButton"
    
    view_faxForwardingScreen = "#HomeScreenAppApplicationStackView"
    view_faxReceiveSettingsScreen = "#faxReceiveMenuList"
    view_ringerVolumeDualLineScreen = "#ringerVolumeDualLineMenuList"
    view_faxReceiveSettingsPaperTrayScreen = "#paperTrayComboBoxpopupList"
    view_fax_receive_settings_fax_receive_speed_screen = "#faxReceiveSpeedComboBoxpopupList"
    view_dualfax_receive_speed_screen = "#faxReceiveSpeedDualLineMenuList"
    view_fax_receive_junk_fax_blocking_screen = "#junkFaxBlocking"
    view_fax_receive_junk_fax_blocking_screen_CallHistory_KeyboardEntry = "#blockedFaxModal"
    view_receive_junk_fax_number_limit_reached_screen = "#maxJunkFaxNumbersLimitReached"
    view_junk_fax_blocking_number_existing_screen = "#NumberAddedExistingListverticalLayout"
    view_enter_junk_fax_number_screen = "#enterJunkFaxNumber"
    blockedFaxScrollBar = "#blockedFaxNumberScrollBar"
    view_enter_junk_fax_number_soho_screen = "#junkFaxAddFaxNumberSoho"
    view_faxSendJobSubmissionScreen = "#DetailPanelverticalLayout"
    view_faxSendRecipientScreen = "#SendFaxAppApplicationStackView"
    view_faxSendRemoveRecipientScreen = "#faxSendRemoveRecipientView"  # Need to be replaced later
    view_faxSetupScreen = "#statusCenterServiceStackView"  
    view_FaxSendToContactsScreen = "#faxSendToContactsView"   # Need to be replaced later
    view_FaxAddressBookScreen = '#contactSelectAddressBookView'
    view_fax_contacts_integration = "#faxContactsIntegrationView"
    view_FaxLocalSelectScreen = '#contactsIntegrationView'
    view_ReceivedCallHistoryScreen = '#receivedFaxCallHistoryView'
    view_fax_contact_list_view = "#contactIntegrationListViewlist1"
    view_fax_received_callhistory_view = "#receivedFaxCallHistoryListViewlist1"
    text_view_empty_record = "#emptyRecordComponent"
    view_faxSendNoContactsAvailableScreen = "#FaxSendNoContactsAvailable"
    view_faxPhoneLineDetailsScreen = "#FaxPhoneLineDetails"   # Need to be replaced later
    view_faxCountryRegionScreen = "#landingPageMenuListListViewlist1"     # Need to be replaced later
    view_faxSelectDialTypeScreen = "#faxSelectDialTypeView"  # Need to be replaced later
    view_keyboard = "#keyboard" 
    view_spicekeyboard = "#spiceKeyboardView"
    view_systemToastMessagesScreen = "#SpiceToast" 
    view_fax_setup_checking_screen = "#CheckingForFaxSetup"
    view_faxReceiveState = "#faxReceiveState"      # Need to be replaced later
    view_faxSetupLineShareScreen = "#faxSetupLineShare"     # Need to be replaced later
    view_faxCheckBasicFaxSetupScreen = "#faxSetupWizard"   # Need to be replaced later
    view_faxSendRecipientsScreen = "#fax_send_recipients_view"     # Need to be replaced later
    view_faxSendContentTypeScreen = "#faxSendContentTypeView"    # Need to be replaced later
    view_faxSetupDistinctiveRingForFaxScreen = "#faxSetupDistinctiveRingForFax"
    view_faxSearchContactScreen = "#searchModelView"
    view_faxConfirmation = "#ConfirmFaxNumberView"  
    view_resolutionListScreen = "#fax_resolutionComboBoxpopupList"
    view_contentTypeListScreen = "#scan_contentTypeComboBoxpopupList"
    view_disntictiveRingsListScreen = "#distinctiveRingComboBoxpopupList"
    view_fax_cancel_setup_screen = "#faxCancelSetup"
    view_fax_setup_answering_machine_screen = "#faxSetupAnsweringMachine"
    view_list_faxToolReports = '#reportListView'
    scrollBar_faxSetup = "#scrollBar"
    scrollBar_faxSettings = "#faxSettingsMenuListScrollBar"
    scrollBar_faxSendSettings = "#faxSendMenuListScrollBar"
    scrollBar_faxReceiveSettings ="#faxReceiveMenuListScrollBar"
    scrollBar_faxDialing = "#faxDialingMenuListScrollBar"
    scrollBar_faxdialing_line1 = "#faxLine1MenuListScrollBar" 
    scrollBar_faxdialing_line2 = "#faxLine2MenuListScrollBar"
    scrollbar_dualfaxdialing = "#faxDialingDualLineMenuListScrollBar"
    scrollBar_faxOptions = "#faxSettingsPageMenuListListViewlist1ScrollBar"
    scrollBar_faxDistinctiveringsOptionListScreen = "#comboBoxScrollBar"
    basic_fax_setup_vertical_layout_scrollbar = "#basicFaxSetupverticalLayoutScrollBar"
    scrollBar_faxToolReports = '#reportListViewScrollBar'
    scrollbar_fax_contact_list_view = "#contactIntegrationListViewlist1ScrollBar"
    scrollbar_fax_receivedcallhistory_list_view = "#receivedFaxCallHistoryListViewlist1ScrollBar"
    view_fax_offhook_phoneline = "#faxOffHookReceiveLandingPage"
    fax_receive_phoneline_button = "#faxOffHookConnectingReceiveButton"
    view_faxReceiveStateScreen = "#incomingFaxAlertverticalLayout"
    fax_dialing_menu_list = "#faxDialingMenuList"
    fax_dialing_line2_menu_list = "#faxDialingDualLineMenuList"
    view_FaxcustomSelectScreen = '#contactsIntegrationView'
    search_icon="#searchButton"
    button_faxAddressbook_custom='#addressbook_test112 #SpiceRadioButton'
    fax_phoneline_not_connected="#phonelineNotConnected"
    fax_phoneline_not_connected_ok_button="#AlertFooter #phonelineNotConnectedokButton"
    fax_contact_search_model_button="#searchModalButton"
    fax_contact_search_text_input_box="#textFieldContainer"
    contact_name_inputtextbox = "#TextInput"
    button_display_button = "#textFieldContainer"
    enter_name_frame="#searchRow"
    fax_access_code="#pinEditor"
    text_field_search_input = "#searchRow #textField"
    button_search = "#searchRow #searchModalButton"
    search_result_section = "#customSection #customSectionOptions #searchResult"
    maximum_contacts_screen = "#maximumContactsExceeded"
    maximum_contacts_screen_ok_button = "#AlertFooter #maximumContactsOkButton"
    fax_Send_Recipients_View = "#faxSendRecipientsView"
    fax_basic_setup_view = "#faxSetupViewModalLayout"

    view_distinctivering_callmachine = "#faxSetupCallFaxMachine"
    distinctive_ring_callmachine_cancel = "#faxSetupCallFaxMachineCancelButton"
    distinctive_ring_callmachine_timeout = "#faxSetupCallTimeoutGrid"
    distinctivering_callmachine_timeoutretry ="#faxSetupCallTimeoutRetryButton"
    distinctivering_callmachine_timeoutcancel ="#faxSetupCallTimeoutCancelButton"
    view_fax_distinctiverecord_cancelscreen = "#faxSetupRingPatternDetectionCancelled"
    distinctiveringrecord_cancelbutton = "#faxSetupRingPatternDetectionCancelledOkButton"
    fax_distinctivering_overwrite_screen = "#faxSetupOverwriteRecordedRingGrid"
    fax_distinctivering_overwrite_proceed = "#FaxSetupOverwriteRecordedRingProceedButton"
    fax_distinctivering_overwrite_cancel = "#FaxSetupOverwriteRecordedRingCancelButton"

    #main settings app scrollbar
    main_settings_app_scrollbar = "#settingsMenuListListViewlist1ScrollBar"
    # Keborad Keys
    press_key_H="#keyH"
    press_key_P="#keyP"
    press_key_T="#keyT"
    press_key_E="#keyE"
    press_key_S="#keyS"
    press_key_ok="#enterKey1"
    press_key_1="#key1"
    press_key_2="#key2"
    press_key_3="#key3"
    press_key_4="#key4"
    press_key_5="#key5"
    press_key_6="#key6"
    press_key_7="#key7"
    press_key_8="#key8"
    press_key_9="#key9"
    press_key_0="#key0"
    press_access_code_done="#doneButton"
    # Header 
    menu_text_readcrumb = "#BreadcrumbView"
    breadcrumb_title_default_text = "#defaultText"
    
    # WIDGETS ON SCREEN : Buttons,text boxes,menu icons etc..

    #Common buttons
    button_home = "#HomeButton"
    button_back = "#BackButton"
    button_back_lower = '#backbutton'
    button_back_close = '#closeButton'
    button_back_close_addressBook = '#closeButton'

    # Fax App
    menu_button_faxApp = "#faxSettingsButton"
    button_allOptions = "#faxAllOptionsButton"
    button_eyeIcon = "#_ExpandButton"
    faxNumberKeyboard = "#faxNumberKeyboard"
    button_faxSetupContinue = "#faxSetupHomeViewContinueButton"    
    menuText_basicFaxSetup = "#basicFaxSetup"   # Need to be replaced later
    menuText_FaxSetup = '#faxDualLineOptionsList'
    button_faxSetupSkip = "#faxSetupHomeViewSkipButton"     
    menuText_FaxSendToContacts = "#faxSendToContacts"     # Need to be replaced later
    faxSendContact1 = "#FaxSendToContact5ab33747-5d83-45b1-8f04-a29008416983"  # Need to be replaced later
    faxSendContact2 = "#FaxSendToContact741f5387-f531-4014-8874-e873d34ce1c1"  # Need to be replaced later
    button_faxSendToContactDone = "#FaxSendToContactDoneButton"  # Need to be replaced later
    menuText_faxEnterFaxNumber = "#FaxEnterFaxNumber"  # Need to be replaced later
    button_faxConfirm  = "#AlertFooter #confirmFaxConfirmButton"
    button_faxSetupNext = "#basicFaxSetupNextButton" # Need to be replaced later
    button_faxSetupCountryLocation = "#locationComboBox"  # Need to be replaced later
    button_faxSend = "#sendFaxButtonFooterMain"
    menuText_dialingPrefix = "#dialingPrefixMenuButton"
    text_toastInfoText = "#infoTextToastMessage"
    button_faxCancel = "#AlertFooter #confirmFaxCancelButton"
    button_dialType = "#dialTypeButton"
    button_phoneLineDetailsNext = "#phoneLineDetailsNextButton"
    button_faxSetUpLineShareNo = "#faxSetupLineShareNoButton"
    button_faxSetUpLineShareYes = "#faxSetupLineShareYesButton"
    button_faxAddressbook_local = '#addressbook_Local #SpiceRadioButton'
    button_faxAddressbook_ldap = '#addressbook_Ldap #SpiceRadioButton'
    button_fax_addressbook_call_history = "#callHistoryListFaxItem"
    button_faxAddressbook_name_select = '#selectButton'
    button_receivedCallHistory_add_select = '#addButton'
    button_faxAddressbook_name_cancel = '#cancelButton'
    button_error_msg_ok = '#okButton'
    button_cancel_junkfax = '#junkFaxNumberCancelButton'
    faxAddressbook_select_error_msg = '#constraintDescription'
    button_faxConfigure = "#AlertFooter #faxConfigureButton"
    button_faxNotConfCancel = "#AlertFooter #cancelButton"
    fax_setup_country_change_button ="#changeLocation"
    ok_change_country = "#OkLocation"
    setup_location_view ="#locationSetup"
    location_next_button = "#nextLocation"
    setup_faxnumber_view = "#faxNumberTextFieldViewModel"
    setup_header_name_view = "#faxHeaderNameTextFieldViewModel"
    faxNumber_next_button = "#nextFaxNumber"
    setup_dialing_prefix_view = "#dialingPrefixTextFieldViewModel"
    dialing_prefix_TextField = "#dialingPrefixTextField"
    dialing_prefix_next_button = "#nextDialingPrefix"
    finish_summary_button = "#finishSummary"
    cancel_confirmation_ok_button = "#faxSetupConfirmationOkButton"
    faxNumber_previous_button = "#previousFaxNumber"
    location_cancel_button = "#cancelLocation #ButtonControl #ContentItem"
    faxNumber_cancel_button = "#cancelFaxNumber"
    cancel_confirmation_view = "#faxSetupConfirmation"
    location_LeftPanel = "#faxLocationLeftPanel"
    dialing_prefix_summary = "#summaryDialingPrefixValue"
    location_summary = "#summaryLocationValue"
    faxnumber_summary = "#summaryFaxNumberValue"
    headername_summary = "#summaryHeaderValue"

    # Tools
    menuText_faxReports = "#reportFaxSettingsTextImage"
    list_checkboxButtonListLayout = "#CheckboxButtonListLayout"
    menuText_faxActivityLog = '#controlObject_report_faxActivityLog'
    view_object_faxActivityLog = '#viewObject_report_faxActivityLog'
    menuText_faxTraceReport = '#controlObject_report_faxTraceReport'
    view_object_faxTraceReport = '#viewObject_report_faxTraceReport'
    menuText_faxJunkReport = '#controlObject_report_junkFaxReport'
    view_object_faxJunkReport = '#viewObject_report_junkFaxReport'
    menuText_faxBillingCodesReport = '#controlObject_report_faxBillingCodeReport'
    view_object_faxBillingCodesReport = '#viewObject_report_faxBillingCodeReport'
    menuText_faxCallReport = '#controlObject_report_faxCallReport'
    view_object_faxCallReport = '#viewObject_report_faxCallReport'
    menuText_faxCallerIDReport = "#controlObject_report_faxCallerIdReport"
    view_object_faxCallerIDReport = "#viewObject_report_faxCallerIdReport"
    button_printMenu = "#printButton"
    button_viewMenu = "#viewButton"
    view_reports_pdf = "#pdfViewGenericStructverticalLayout"
    addressbook_name_common = '#checkBox_'
    fax_report_list_view = "#reportListView"
    fax_contact_reset_button="#resetButton"

    # Fax Options Screen Widgets
    view_constraint_message = "#ConstraintMessage"
    ok_button_constrained_message = "#okButton"
    combo_box_twosided_format = "#scan_twoSidedFormatMenuComboBox"
    combo_box_twosided_settings_format = "#SettingsSpiceComboBox"
    combo_box_popuplist = "#SettingsSpiceComboBoxpopupList"
    combo_box_book_style = "#BookStyle"
    combo_box_flip_style = "#FlipStyle"
    combo_box_2sidedOriginal = "#scan_2sidedOriginalComboBox"
    combo_box_row_2sidedOriginal = "#scan_2sidedOriginalSettingsComboBox"
    combo_box_options_simplex = "#ComboBoxOptionssimplex"
    combo_box_options_duplex = "#ComboBoxOptionsduplex"
    slider_lighterDarker = "#scan_lighterDarkerMenuSlider"
    slider_row_lighterDarker = "#scan_lighterDarkerSettingsSlider"
    slider_sharpness = "#scan_sharpnessMenuSlider"
    slider_row_sharpness = "#scan_sharpnessSettingsSlider"
    slider_contrast = "#scan_contrastMenuSlider"
    slider_row_contrast = "#scan_contrastSettingsSlider"
    slider_backgroundcleanup = "#scan_backGroundCleanUpMenuSlider"
    slider_row_backgroundcleanup = "#scan_backGroundCleanUpSettingsSlider"
    button_faxSettings = "#FaxSettingsButton"
    row_object_contentType = "#scan_contentTypeSettingsComboBox"
    combo_box_contentType = "#scan_contentTypeComboBox"
    combo_box_contentType_scrollbar = "#comboBoxScrollBar"
    combo_contentTYpe_option_mixed = "#ComboBoxOptionsmixed"
    combo_contentTYpe_option_photograph = "#ComboBoxOptionsphoto"
    combo_contentTYpe_option_text = "#ComboBoxOptionstext"
    combo_contentTYpe_option_undefined = "#ComboBoxOptionsundefined"
    combo_contentTYpe_option_automatic = "#ComboBoxOptionsautomatic"
    combo_contentTYpe_option_image = "#ComboBoxOptionsimage"

    original_sides_custom_dict = {
        "simplex": ["c1Sided", "#RadioButtonOptionssimplex"],
        "duplex": ["c2Sided", "#RadioButtonOptionsduplex"]
    }
    row_object_OriginalSides = "#originalSidesSettings"
    row_object_OriginalSides_custom_2info_block = "#originalSidesSettings_2infoBlockRow"
    fax_options_OriginalSides_View = "#originalSidesSettingsView"
    scrollbar_original_sides_View = "#originalSidesSettingsViewScrollBar"
    original_sides_auto_checkbox = "#CheckBoxOptionsOriginalSidesAuto"
    row_originalSidesAuto_option = "#OriginalSidesAuto"
    row_originalSidesSimplex_option = "#simplexButton"
    row_originalSidesDuplex_option = "#duplexButton"

    row_object_resolution =  "#fax_resolutionSettingsComboBox"
    combo_box_resolution = "#fax_resolutionComboBox"
    combo_resolution_option_Standrad = "#ComboBoxOptionsstandard"
    combo_resolution_option_Fine = "#ComboBoxOptionsfine"
    combo_resolution_option_Superfine ="#ComboBoxOptionssuperfine"

    view_faxSettings_originalSize = "#scan_originalSizeMenuSelectionList"
    fax_originalSize_scrollbar = "#scan_originalSizeMenuSelectionListScrollBar"
    list_faxSettings_originalSize = "#scan_originalSizeSettingsTextImage"
    fax_option_header_section = "#SpiceHeaderVar2"
    original_size_value = "#scan_originalSizeSettingsTextImage_2infoBlockRow #contentItem"
    original_size_back_button = "#scan_originalSizeMenuSelectionList #BackButton"
    contentType_Value = "#scan_contentTypeComboBox #contentItem"

    fax_mediasize_letter_str_id = "cMediaSizeIdLetter"
    fax_mediasize_any_str_id = "cMediaSizeIdAny"

    radio_original_size_any="#MenuValueany"
    radio_originalSize_mixed_letter_legal = "#MenuValuecom_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_legal"
    radio_originalSize_mixed_letter_ledger = "#MenuValuecom_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_ledger"
    radio_originalSize_mixed_a4_a3 = "#MenuValuecom_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_a4_dash_a3"
    radio_originalSize_na_letter_8_5x11in = "#MenuValuena_letter_8_dot_5x11in"
    radio_originalSize_rotate_na_letter_8_5x11in = "#MenuValuecom_dot_hp_dot_ext_dot_mediaSize_dot_na_letter_8_dot_5x11in_dot_rotated"  
    radio_originalSize_na_legal_8_5x14in = "#MenuValuena_legal_8_dot_5x14in"
    radio_originalSize_na_executive_7_dot_25x10_dot_5in = "#MenuValuena_executive_7_dot_25x10_dot_5in"
    radio_originalSize_invoice_5_5x8_5in = "#MenuValuena_invoice_5_dot_5x8_dot_5in"
    radio_originalSize_tabloid_11x17 = "#MenuValuena_ledger_11x17in"
    radio_originalSize_3x5in = "#MenuValuena_index_dash_3x5_3x5in"
    radio_originalSize_index_4x6_4x6in = "#MenuValuena_index_dash_4x6_4x6in"
    radio_originalSize_5x7in = "#MenuValuena_5x7_5x7in"
    radio_originalSize_index_5x8_5x8in = "#MenuValuena_index_dash_5x8_5x8in"
    radio_originalSize_na_foolscap_8_dot_5x13in= "#MenuValuena_foolscap_8_dot_5x13in"
    radio_originalSize_oficio_216x340 = "#MenuValuena_oficio_8_dot_5x13_dot_4in"
    radio_originalSize_a3 = "#MenuValueiso_a3_297x420mm"
    radio_originalSize_iso_a4_210x297mm = "#MenuValueiso_a4_210x297mm"
    radio_originalSize_rotate_iso_a4_210x297mm = "#MenuValuecom_dot_hp_dot_ext_dot_mediaSize_dot_iso_a4_210x297mm_dot_rotated"
    radio_originalSize_iso_a5_148x210mm = "#MenuValueiso_a5_148x210mm"
    radio_originalSize_rotate_iso_a5_148x210mm = "#MenuValuecom_dot_hp_dot_ext_dot_mediaSize_dot_iso_a5_148x210mm_dot_rotated"
    radio_originalSize_iso_a6_105x148mm = "#MenuValueiso_a6_105x148mm"
    radio_originalSize_iso_ra4_215x305mm = "#MenuValueiso_ra4_215x305mm"
    radio_originalSize_b4 = "#MenuValuejis_b4_257x364mm"
    radio_originalSize_jis_b5_182x257mm = "#MenuValuejis_b5_182x257mm"
    radio_originalSize_rotate_jis_b5_182x257mm = "#MenuValuecom_dot_hp_dot_ext_dot_mediaSize_dot_jis_b5_182x257mm_dot_rotated"
    radio_originalSize_jis_b6_128x182mm = "#MenuValuejis_b6_128x182mm"
    radio_originalSize_om_16k_195x270mm = "#MenuValueom_16k_195x270mm"
    radio_originalSize_16k_184x260 = "#MenuValueom_16k_184x260mm"
    radio_originalSize_16k_197x273 = "#MenuValueroc_16k_7_dot_75x10_dot_75in"
    radio_originalSize_double_postcard_jis_148x200mm = "#MenuValuejpn_oufuku_148x200mm"
    radio_originalSize_10x15 = "#MenuValueom_small_dash_photo_100x150mm"
    radio_originalSize_5x5in = "#MenuValueoe_square_dash_photo_5x5in"

    row_original_size_any= "#anyscan_originalSize"
    row_originalSize_mixed_letter_legal = "#com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_legalscan_originalSize"
    row_originalSize_mixed_letter_ledger = "#com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_letter_dash_ledgerscan_originalSize"
    row_originalSize_mixed_a4_a3 = "#com_dot_hp_dot_ext_dot_mediaSize_dot_mixed_dash_a4_dash_a3scan_originalSize"
    row_original_size_na_letter_8_5x11in = "#na_letter_8_dot_5x11inscan_originalSize"
    row_original_size_rotate_na_letter_8_5x11in = "#com_dot_hp_dot_ext_dot_mediaSize_dot_na_letter_8_dot_5x11in_dot_rotatedscan_originalSize"
    row_original_size_na_legal_8_5x14in = "#na_legal_8_dot_5x14inscan_originalSize"
    row_original_size_executive_7_25x10_5in = "#na_executive_7_dot_25x10_dot_5inscan_originalSize"
    row_original_size_invoice_5_5x8_5in = "#na_invoice_5_dot_5x8_dot_5inscan_originalSize"
    row_original_size_tabloid_11x17 = "#na_ledger_11x17inscan_originalSize"
    row_original_size_3x5in = "#na_index_dash_3x5_3x5inscan_originalSize"
    row_original_size_index_4x6_4x6in = "#na_index_dash_4x6_4x6inscan_originalSize"
    row_original_size_5x7in = "#na_5x7_5x7inscan_originalSize"
    row_original_size_index_5x8_5x8in = "#na_index_dash_5x8_5x8inscan_originalSize"
    row_original_size_foolscap_8_5x13in = "#na_foolscap_8_dot_5x13inscan_originalSize"
    row_original_size_oficio_216x340 = "#na_oficio_8_dot_5x13_dot_4inscan_originalSize"
    row_original_size_a3 = "#iso_a3_297x420mmscan_originalSize"
    row_original_size_rotate_iso_a4_210x297mmn = "#com_dot_hp_dot_ext_dot_mediaSize_dot_iso_a4_210x297mm_dot_rotatedscan_originalSize"
    row_original_size_iso_a5_148x210mm = "#iso_a5_148x210mmscan_originalSize"
    row_original_size_rotate_iso_a5_148x210mm = "#com_dot_hp_dot_ext_dot_mediaSize_dot_iso_a5_148x210mm_dot_rotatedscan_originalSize"
    row_original_size_iso_a6_105x148mm = "#iso_a6_105x148mmscan_originalSize"
    row_original_size_iso_ra4_215x305mmscan_originalSize = "#iso_ra4_215x305mmscan_originalSize"
    row_original_size_b4 = "#jis_b4_257x364mmscan_originalSize"
    row_original_size_jis_b5_182x257mm = "#jis_b5_182x257mmscan_originalSize"
    row_original_size_rotate_jis_b5_182x257mm = "#com_dot_hp_dot_ext_dot_mediaSize_dot_jis_b5_182x257mm_dot_rotatedscan_originalSize"
    row_original_size_jis_b6_128x182mm = "#jis_b6_128x182mmscan_originalSize"
    row_original_size_16k_195x270 = "#om_16k_195x270mmscan_originalSize"
    row_original_size_16k_184x260 = "#om_16k_184x260mmscan_originalSize"
    row_original_size_16k_197x273 = "#roc_16k_7_dot_75x10_dot_75inscan_originalSize"
    row_original_size_double_postcard_jis_148x200mm = "#jpn_oufuku_148x200mmscan_originalSize"
    row_original_size_iso_a4_210x297mmn = "#iso_a4_210x297mmscan_originalSize"
    row_original_size_10x15 = "#om_small_dash_photo_100x150mmscan_originalSize"
    row_original_size_5x5in = "#oe_square_dash_photo_5x5inscan_originalSize"

    switch_includecoverpage_row = "#fax_includeCoverPageMenuSwitch"
    switch_includecoverpage_button = "#includeCoverPage"
    fax_option_header_setion = "#SpiceHeaderVar2"

    row_object_scan_blank_page_suppression = "#scan_blankPageSuppressionSettingsComboBox"
    combo_scan_blank_page_suppression = "#scan_blankPageSuppressionComboBox"
    view_can_blank_page_suppression_list = "#scan_blankPageSuppressionComboBoxpopupList"
    combo_blank_page_suppression_option_On = "#ComboBoxOptionstrue_"
    combo_blank_page_suppression_option_Off = "#ComboBoxOptionsfalse_"

    row_object_content_orientation = "#scan_contentOrientationSettingsComboBox"
    settings_content_orientation = "#scan_contentOrientationComboBox"
    view_settings_orientation_screen = "#scan_contentOrientationComboBoxpopupList"
    orientation_landscape_option = "#ComboBoxOptionslandscape"
    orientation_portrait_option = "#ComboBoxOptionsportrait"

    row_object_fax_line_selection = "#scan_faxlineselectionMenuComboBox"
    combo_fax_line = "#SettingsSpiceComboBox #contentItem"
    view_fax_line_list = "#SettingsSpiceComboBoxpopupList"
    combo_fax_line_option_auto = "#ComboBoxOptionsAuto"
    combo_fax_line_option_line1 = "#ComboBoxOptionsLine1"
    combo_fax_line_option_line2 = "#ComboBoxOptionsLine2"

    view_constraint_message = "#ConstraintMessage"
    ok_button_constrained_message = "#okButton"

    #Fax Settings(Menu)
    button_menuFaxSettings = "#faxSettingsSettingsTextImage" 
    menuText_faxSend = "#faxSendSettingsTextImage"
    menuText_faxReceive = "#faxReceiveSettingsTextImage"
    view_menu_fax_settings = "#faxSettingsMenuList"
    button_menu_fax_setup = "#faxSetupMenuButton"
    view_menu_fax_forwarding_list = "#faxForwardingMenuList "

    receive_speed_combobox_dual_fax ="#faxReceiveSpeedDualLineSettingsTextImage_2infoBlockRow"
    view_receive_dual_fax = "#faxReceiveSpeedDualLineMenuList"
    receive_speed_line1_combobox ="#line1FaxReceiveSpeedSettingsComboBox #line1FaxReceiveSpeedComboBox"
    receive_speed_line2_combobox ="#line2FaxReceiveSpeedSettingsComboBox #line2FaxReceiveSpeedComboBox"
    receive_speed_combobox_popuplist = "#line1FaxReceiveSpeedComboBoxpopupList"
    receive_speed_scrollbar ="ScrollBarRectangle"
    receive_speed_dual_fax ={
        "fast": "#ComboBoxOptionsfast #infoBlockRow #contentItem",
        "medium": "#ComboBoxOptionsmedium #infoBlockRow #contentItem",
        "slow": "#ComboBoxOptionsslow #infoBlockRow #contentItem",
    }

    menu_button_fax_settings_clearFaxLogs = "#clearFaxActivityLog"
    menu_button_fax_settings_clearLogs = "#clearFaxLogMemoryModel"
    view_fax_settings_clearfax_log = "#clearFaxLogMemoryView"
    menu_button_fax_settings_clearLogs_clear = "#clearFaxButton"
    menu_button_fax_settings_clearLogs_cancel = "#cancelButton"
    view_settings_toast_window = "#ToastWindowToastStackView"
    view_settings_fax_toastinfo = "#infoTextToastMessage"

    # Fax Setup

    home_button_basic_fax_setup = "#basicFaxSetup #HomeButton"
    button_basicFaxSetupNext = "#basicFaxSetupNextButton"  # Need to be replaced later
    menuText_faxSetup = "#faxSetupSettingsTextImage" 
    fax_basic_required_text = "#basicFaxSetupRequired"
    button_faxSetupFaxHeaderName = "#faxHeaderNameTextField"   # Need to be replaced later
    input_enterFaxHeaderName = "#faxHeaderNameTextField"
    input_faxSetupFaxNumber = "#faxNumberTextField"
    button_faxSetupFaxNumber = "#faxNumberTextField"  # Need to be replaced later
    button_dialType = "#dialTypeButton"
    view_faxSetupVoiceCalls_screen = "#faxSetupVoiceCalls"
    button_faxSetUpVoiceCallsYes = "#faxSetupVoiceCallsYesButton"
    button_faxSetUpVoiceCallsNo = "#faxSetupVoiceCallsNoButton"
    button_faxCheckAlertOK = "#OK"
    button_faxSetUpDistinctiveRingYes = '#faxSetupDistinctiveRingForFaxYesButton #ButtonControl'
    button_faxSetUpDistinctiveRingNo = '#faxSetupDistinctiveRingForFaxNoButton #ButtonControl'
    button_faxSetupMenuButton = '#faxSetupButtonModel'
    view_faxSetupMenuLine1 = '#faxLine1'
    view_faxSetupMenuLine2 = '#faxLine2'
    basic_fax_setup_required_ok_button = "#faxSetupWizard #okButton"
    button_fax_setup_answering_machine_yes = "#faxSetupAnsweringMachineYesButton #ButtonControl"
    button_fax_setup_answering_machine_no = "#faxSetupAnsweringMachineNoButton #ButtonControl"
    button_fax_complete_ok_button = "#faxSetupCompleteOkButton"
    button_fax_cancel_setup_yes = "#AlertFooter #faxCancelSetupYesButton"
    view_basic_fax_setup_header ="#basicFaxSetupHeaderView"
    item_fax_country_text = "#countryList_firstinfoBlockRow"
    select_fax_country_label = "#countryList"
    input_faxheader_name_view ="#faxHeaderNameTextFieldViewModel"
    input_fax_header_name_text = "#faxHeaderNameTextLabel"
    input_fax_header_name_label = "#faxHeaderNameTextField"
    input_fax_number_text = "#faxNumberTextLabel"
    input_fax_number_view = "#faxNumberTextFieldViewModel"
    input_fax_number_label = "#faxNumberTextField"
    view_junk_block_empty_descr =  "#junkFaxBlocking #contentItem"

    view_send_fax_notifications = "#FaxSendNotificationView"
    notification_option_job_failed = "#onJobFailed"
    notification_option_job_completed = "#onJobCompleted"
    notification_option_never = "#never"
    notification_done_button = "#doneButton"
    notification_cancel_button = "#FaxSendNotificationView #cancelButton"
    include_thumbnail = "#includeThumbnailSpiceCheckBox"
    include_thumbnail_view = "#CheckBoxView"
    fax_send_notification_row = "#FaxSendNotification_2infoBlockRow"
    scrollBar_fax_send_notification = "#FaxSendNotificationViewlist1ScrollBar"
    scrollBar_fax_send_notification_view = "#notificationListViewScrollBar"


    # send fax settings for notification options
    combo_box_send_fax_notifications = "#sendFaxNotificationsComboBoxpopupList"
    combo_option_job_failed = "#ComboBoxOptionsonJobFailed"
    combo_option_job_completed = "#ComboBoxOptionsonJobCompleted"
    combo_option_never = "#ComboBoxOptionsnever"
    item_fax_notifications = "#contentItem"
    fax_send_notification_time_out = "#faxSendNotificationTimeout"
    fax_send_notification_time_out_yes_btn = "#FaxSendNotificationTimeoutYesButton"
    fax_send_notification_time_out_no_btn = "#FaxSendNotificationTimeoutNoButton"

    # receive fax settings for notification options
    combo_box_receive_fax_notifications = "#receiveFaxNotificationsComboBoxpopupList"
    view_recieve_fax_notifications = "#FaxReceiveNotificationView"
    notification_receive_done_button = "#doneReceiveNotificationButton"
    fax_receive_notification_row = "#FaxReceiveNotification_2infoBlockRow"
    receive_include_thumbnail = "#includeThumbnailReceiveSpiceCheckBox"
    scrollBar_fax_receive_notification = "#FaxReceiveNotificationViewlist1ScrollBar"
    view_faxreceive_notification = "#FaxReceiveNotificationView"

    #Send fax settings page
    menuText_faxDialing = "#faxDialingSettingsTextImage"
    menuText_faxDialing_line2 = "#faxLine2SettingsTextImage #faxLine2SettingsTextImage_firstinfoBlockRow"
    menuText_faxDialing_line1 = "#faxLine1SettingsTextImage #faxLine1SettingsTextImage_firstinfoBlockRow"

    fax_send_menu_list = "#faxSendMenuList"

    menuSwitch_pulseDialingMode = "#pulseDialingModeSettingsSwitch"
    toggle_pulse_dialing_mode = "#pulseDialingModeMenuSwitch"
    row_menuSwitch_scanAndFaxMethod = "#scanAndFaxMethodSettingsSwitch"
    menuSwitch_scanAndFaxMethod = "#scanAndFaxMethodMenuSwitch"
    row_menuSwitch_faxNumberConfirmation = "#faxNumberConfirmationSettingsSwitch"
    menuSwitch_faxNumberConfirmation = "#faxNumberConfirmationMenuSwitch"
    row_menuSwitch_pcSendFax = "#pcSendFaxSettingsSwitch"
    menuSwitch_pcSendFax = "#pcSendFaxMenuSwitch"
    errorCorrectionModeTextImage = "#errorCorrectionModeDualFaxSettingsTextImage"
    dual_fax_errorcorrection_mode = "#errorCorrectionModeDualFaxSettingsTextImage_2infoBlockRow"
    dual_fax_errorcorrection_mode_line1 ="#errorFaxLine1MenuSwitchspiceSwitch"
    dual_fax_errorcorrection_mode_line2 = "#errorFaxLine2MenuSwitchspiceSwitch"
    view_dual_fax_errorcorrection_mode = "#errorCorrectionModeDualFaxMenuList"
    dual_fax_row_dial_type = "#pulseDialingModeSettingsComboBox"
    dual_fax_dial_type_combo_box = "#pulseDialingModeComboBox "
    row_menuSwitch_errorCorrectionMode = "#errorCorrectionModeSettingsSwitch"
    menuSwitch_errorCorrectionMode = "#errorCorrectionModeMenuSwitch"
    row_menuSwitch_line2_errorCorrectionMode = "#errorFaxLine2SettingsSwitch"
    menuSwitch_line2_errorCorrectionMode = "#errorFaxLine2MenuSwitch"
    row_menuSwitch_overLayFaxHeader ="#overlayFaxHeaderSettingsSwitch"
    menuSwitch_overLayFaxHeader = "#overlayFaxHeaderMenuSwitch"
    row_menuSwitch_billingCode = "#billingCodeSettingsSwitch"
    menuSwitch_billingCode = "#billingCodeMenuSwitch"
    button_resolution = "#resolutionButton"
    button_contentType = "#contentTypeButton"
    row_switch_fax_send_speed = "#faxSendSpeedSettingsComboBox"
    button_switch_fax_send_speed = "#faxSendSpeedComboBox"
    button_switch_fax_send_speed_line2 = "#faxSendSpeed_line2ComboBox"
    view_fax_send_speed_option = "#faxSendSpeedComboBoxpopupList"
    row_dialing_prefix = "#dialingPrefixWFSettingsTextField"
    text_field_dialing_prefix = "#dialingPrefixWFMenuTextField"
    item_in_text_field_dialing_prefix = "#ContentItem"
    button_clear_field = "#ClearMouseArea"
    billing_code_ok_button = "#billingCodeOkButton"
    billing_code_cancel_button = "#billingCodeCancelButton"
    billing_code_screen = "#billingCode"
    help_text_locator = "#HelperText"
    combo_box_send_fax_line_selection = "#sendFaxLineSelectionComboBox #textColumn #contentItem"
    row_menuComboBox_overLayFaxHeader ="#overlayFaxHeaderSettingsComboBox"
    menuComboBox_overLayFaxHeader = "#overlayFaxHeaderComboBox"
    row_switch_fax_line_monitor_volume = "#lineMonitorVolumeSettingsComboBox"
    button_switch_fax_line_monitor_volume = "#lineMonitorVolumeComboBox"
    line_monitor_combo_list = "#lineMonitorVolumeComboBoxpopupList"

    row_switch_fax_pulse_dialing_mode = "#pulseDialingModeSettingsComboBox"
    button_switch_fax_pulse_dialing_mode = "#pulseDialingModeComboBox"
    pulse_dialing_combo_list = "#pulseDilaingComboBoxpopupList"

    #Receive fax  settings page

    combobox_twosided_format_option = "#twoSidedFormatMenuComboBox"
    combobox_twosided_format_bookstyle = "#BookStyle"
    combobox_twosided_format_flipstyle = "#FlipStyle"
    menuText_distinctiveRing = "#distinctiveRingMenuButton"   #Need to be replaced later
    fax_distinctive_ring_settings = "#faxDRPDinSettings"
    fax_distinctive_ring_settings_select_btn = "#selectDRPDValue"
    fax_junk_fax_blocking_settings = "#checkJunkFaxBlockingNumber"
    fax_receive_fax_notifications_settings = "#receiveFaxNotificationsSettingsComboBox"
    fax_receive_fax_notifications_combo_box_option = "#FaxReceiveNotification"
    fax_send_fax_notifications_settings = "#sendFaxNotificationsSettingsComboBox"
    fax_send_fax_nofifications_combo_box_option = "#FaxSendNotification"
    menuText_faxForwarding = "#faxForwardingSettingsTextImage" 
    menuText_paperTray = "#paperTrayMenuTextImageBranch"
    menuSwitch_autoAnswer = "#autoAnswerMenuSwitch"
    row_menuSwitch_autoAnswer = "#autoAnswerSettingsSwitch"
    row_menuSwitch_errorCorrectionMode_receive = "#errorCorrectionSettingsSwitch"
    menuSwitch_errorCorrection_receive  = "#errorCorrectionMenuSwitch"
    row_menuSwitch_twoSidedPrinting_receive = "#twoSidedPrintingSettingsSwitch"   
    menuSwitch_twoSidedPrinting_receive = "#twoSidedPrintingMenuSwitch"
    spiceSwitch_twoSidedPrinting_receive = "#twoSidedPrintingMenuSwitchspiceSwitch"
    row_menuSwitch_stampReceivedFaxes_receive = "#stampReceivedFaxesSettingsSwitch"
    menuSwitch_stampReceivedFaxes_receive = "#stampReceivedFaxesMenuSwitch"
    spiceSwitch_stampReceivedFaxes_receive = "#stampReceivedFaxesMenuSwitchspiceSwitch"
    row_menuSwitch_fitToPage_receive = "#automaticReductionSettingsSwitch"
    menuSwitch_fitToPage_receive = "#automaticReductionMenuSwitch"
    spiceSwitch_fitToPage_receive = "#automaticReductionMenuSwitchspiceSwitch"
    row_menu_switch_detect_dial_tone_receive = "#detectDialToneSettingsSwitch"
    menu_switch_detect_dial_tone_receive = "#detectDialToneMenuSwitch"

    menuText_ringerVolumeMenu_receive = "#ringerVolumeMenuButton"
    menuText_paperTraySelection_receive = "#MenuSelectionListpaperTray"

    slider_row_redialOnError = "#redialOnErrorSettingsSlider"
    slider_redialOnError =  "#redialOnErrorMenuSlider"
    slider_row_redialOnNoAnswer = "#redialOnNoAnswerSettingsSlider"
    slider_redialOnNoAnswer ="#redialOnNoAnswerMenuSlider" 
    slider_row_redialOnBusy = "#redialOnBusySettingsSlider"
    slider_redialOnBusy = "#redialOnBusyMenuSlider"
    slider_row_redialInterval ="#redialIntervalSettingsSlider"
    slider_redialInterval ="#redialIntervalMenuSlider"
    spinbox_ringsToAnswer = "#ringsToAnswerMenuSpinBox"
    combobox_ring_to_answer = "#ringsToAnswerDualLineSettingsTextImage_2infoBlockRow"
    view_ringtoanswer_dualfax ="#ringsToAnswerDualLineMenuList"
    spinbox_line1ringsToAnswer = "#line1RingsToAnswerMenuSpinBox"
    spinbox_line2ringsToAnswer = "#line2RingsToAnswerMenuSpinBox"
    combo_box_distinctiveRings = "#distinctiveRingComboBox"
    row_object_distinctiveRings = "#distinctiveRingSettingsComboBox"
    combo_distinctiveRing_option_singleRing ="#ComboBoxOptionsSingleRing"
    combo_distinctiveRing_option_doubleRings = "#ComboBoxOptionsDoubleRing"
    combo_distinctiveRing_option_tripleRings = "#ComboBoxOptionsTripleRing"
    combo_distinctiveRing_option_doublandTriplerings = "#ComboBoxOptionsDoubleAndTripleRing"
    combo_distinctiveRing_option_useRecordedRing = "#ComboBoxOptionsRecordedRingPattern"
    combo_distinctiveRing_option_allStandardRings = "#ComboBoxOptionsAllStandardRings"
    combo_distinctiveRing_option_ringPatternDetection = "#ComboBoxOptionsStartRecord"
    distinctive_ring_menu_item_double_ring = "#DoubleRing"
    distinctive_ring_menu_item_single_ring = "#SingleRing"
    distinctive_ring_menu_item_triple_ring = "#TripleRing"
    distinctive_ring_menu_item_double_and_triple_ring = "#DoubleAndTripleRing"
    distinctive_ring_menu_item_use_recorded_ring = "#RecordedRingPattern"
    distinctive_ring_menu_item_all_standard_rings = "#AllStandardRings"
    distinctive_ring_menu_item_start_record = "#StartRecord"

    distinctive_ring_menu_list = "#faxSetupDistinctiveRingTypeView"
    distinctive_ring_menu_list_scrollbar = "#SpiceListViewViewScrollBar"

    view_distinctivering_recorded_success = "faxSetupDistinctiveRingRecordComplete"
    distinctivering_recorded_success_ok = "faxSetupDistinctiveRingRecordCompleteNextButton"

    combo_box_fax_receive_speed_slow = "#ComboBoxOptionsslow"
    combo_box_fax_receive_speed_medium = "#ComboBoxOptionsmedium"
    combo_box_fax_receive_speed_fast = "#ComboBoxOptionsfast"

    combo_box_dualfax_receive_speed_slow = "#ComboBoxOptionsslow #infoBlockRow #contentItem"
    combo_box_dualfax_receive_speed_medium = "#ComboBoxOptionsmedium #infoBlockRow #contentItem"
    combo_box_dualfax_receive_speed_fast = "#ComboBoxOptionsfast #infoBlockRow #contentItem"

    combo_box_dualfax_send_speed_slow = "#ComboBoxOptionsslow #infoBlockRow #textColumn #contentItem"
    combo_box_dualfax_send_speed_medium = "#ComboBoxOptionsmedium #infoBlockRow #textColumn #contentItem"
    combo_box_dualfax_send_speed_fast = "#ComboBoxOptionsfast #infoBlockRow #textColumn #contentItem"

    combo_box_fax_send_line_monitor_volume_low = "#ComboBoxOptionslow"
    combo_box_fax_send_line_monitor_volume_high = "#ComboBoxOptionshigh"
    combo_box_fax_send_line_monitor_volume_off = "#ComboBoxOptionsoff"

    combo_box_fax_send_pulse_dialing_pulse = "#ComboBoxOptionspulse"
    combo_box_fax_send_pulse_dialing_tone = "#ComboBoxOptionstone"
    
    # Fax send
    button_faxNumberOfRecipientsButton = "#FaxNumberOfRecipientsButton"  #Need to be replaced later
    menuText_recipient2 = "#FaxRecipient{a1e37040-f0b4-4934-8c45-a0049ee2c978}"
    button_faxSendRecipientsRemoveButton = "#FaxSendRecipentsRemoveButton"
    button_FaxNoListAvailableNo = "#FaxNoListAvailableNoButton"
    button_faxNoListAvailableYes = "#FaxNoListAvailableYesButton"
    button_faxAddRecipients = "#FaxAddRecipientsButton"
    textField_enterFaxNumberSendScreen = "#enterFaxNumberTextField"
    textField_enterFaxDialingPrefixNumberSendScreen = "#faxNumberPrefixTextField"
    dialing_prefix_homepro = "#dialingPrefixValue"
    test_field_enterBillingCodeTextField = "#enterBillingCodeTextField1 #TextInputBox"
    enter_junk_fax_number_text_field = "#enterjunkFaxNumberTextField"
    fax_complete_wizard_screen = "#ActiveJobModalView"          #"#wizardCompletionActiveJob"
    fax_send_start_screen = "#wizardProgressActiveJob"

    # Fax Receive

    button_incomingFaxAccept  = "#accpetReceiveFax"
    button_incomingFaxIgnore = "#ignoreReceiveFax"
    receive_fax_job_completion_screen = "#wizardProgressRecevieActiveJob"

    # Junk Fax Blocking
    view_number_existing_screen = "#NumberAddedExistingList"
    view_enter_junk_fax_number = "#enterJunkFaxNumber"
    view_numbers_added_to_junk_list = "#numbersAddedToJunkList"
    view_number_already_junk_fax_view = "#numberAlreadyJunkFaxView"
    view_junk_fax_number_removed = "#numberRemovedFromJunkFax"
    body_view_number_already_junk_fax = "#numberAlreadyJunkFaxView #alertDetailDescription #contentItem"

    ok_button_junk_fax = "#AlertFooter #junkFaxOkButton"
    add_button_junk_fax = "#junkFaxAddButton"
    # receivedCallHistory_button_junk_fax = "#receivedCallHistory"
    receivedCallHistory_button_junk_fax = "#SpiceButton"
    keyboardEntry_button_junk_fax = "#enterUsingKeyboard"
    cancel_button_receivedCallHistory = "#cancelButton"
    ok_button_junk_fax_number = "#junkFaxNumberOkButton"
    ok_button_soho_junk_fax_number = "#junkFaxAddFaxNumberSohoOkButton"
    cancel_button_soho_junk_fax_number = "#junkFaxAddFaxNumberSohoCancelButton"
    ok_button_numbers_added_to_junk_list = "#AlertFooter #numbersAddedToJunkListokButton"
    add_button_blocked_number = "#blockedNumberAddButton"
    remove_button = "#removeButton"
    selectAll_checkbox = "#selectAllAction"
    button_add_last_sender = "#lastSenderButton"
    ok_button_already_junk_fax_number = "#AlertFooter #numberAlreadyJunkFaxViewokButton"
    ok_button_on_max_junk_fax_number_alert = "#AlertFooter #maxJunkFaxNumbersLimitReachedokButton"
    ok_button_junk_fax_number_removed = "#AlertFooter #numbersFromJunkListokButton"

    # Fax Forward

    menuSwitch_faxForward = "#forwardEnabledMenuSwitch"
    menuSwitch_faxForwardAndPrint = "#forwardPrintEnabledMenuSwitch" 
    menuText_forwardNumber = "#forwardNumberMenuButton"   # Need to be replaced later
    button_faxForward = "#[[]]"
    textField_faxNumberSettings = "#forwardNumberWFSettingsTextField"
    textField_enterFaxnumber = "#forwardNumberWFMenuTextField"
    textField_mouse_area = "#flickableMouseArea"
    item_in_textField_enterFaxnumber = "#ContentItem"
  
    #Keyboard_keys
    key_board_keys="#key"
    keyEnter = "#hideKeyboardKey"
    key123  = "#symbolModeKey"
    keyOK = "#keyOk"
    KeyOK_two = '#enterKey1'
    enter_key_number_keyboard = "#enterKey"
    KeyPause = '#pause'
    key_back_space = "#backspaceKey"
    key_hide_keyboard="#hideKeyboardKey"
    
    # Settings
    button_menu_settings_app = "#settingsSettingsButton"
    view_menu_settings_screen = "#settingsMenuListListViewlist1"

    # Fax Receive Settings
    combo_box_paper_tray = "#paperTrayComboBox"
    row_object_paper_tray = "#paperTraySettingsComboBox"
    paper_tray_dic = {
        "Tray": "#ComboBoxOptionsmain",
        "Tray1": "#ComboBoxOptionstray_dash_1 #SpiceRadioButton",
        "Tray2": "#ComboBoxOptionstray_dash_2 #SpiceRadioButton",
        "Tray3": "#ComboBoxOptionstray_dash_3 #SpiceRadioButton",
        "Automatic": "#ComboBoxOptionsauto_ #SpiceRadioButton"
    }

    
    paper_tray_dic_enterprise = {
        "Tray": "#ComboBoxOptionsmain",
        "Tray1": "#ComboBoxOptionstray_dash_1",
        "Tray2": "#ComboBoxOptionstray_dash_2",
        "Tray3": "#ComboBoxOptionstray_dash_3",
        "Automatic": "#ComboBoxOptionsauto_"
    }

    combo_box_fax_receive_speed = "#faxReceiveSpeedComboBox"
    row_object_fax_receive_speed = "#faxReceiveSpeedSettingsComboBox"

    combo_box_line2_fax_receive_speed = "#line2FaxReceiveSpeedComboBox"
    view_line2_receive_speed_Screen = "#line2FaxReceiveSpeedComboBoxpopupList"

    combo_box_line2_ringer_volume = "#line2RingerVolumeComboBox"
    row_object_line2_ringer_volume = "#line2RingerVolumeSettingsComboBox"
    view_line2_ringer_volume_Screen = "#line2RingerVolumeComboBoxpopupList"

    combo_box_ringer_volume = "#ringerVolumeComboBox"
    row_object_ringer_volume = "#ringerVolumeSettingsComboBox"
    ringer_volume_scrollbar = "#comboBoxScrollBar"
    view_faxReceiveSettings_ringer_volume_Screen = "#ringerVolumeComboBoxpopupList"
    ringer_volume_dict = {
        "Low": "#ComboBoxOptionslow",
        "High": "#ComboBoxOptionshigh",
        "Off": "#ComboBoxOptionsoff"
    }
    rowObjectCountryRegion = "#locationTextRowLayout"
    comboBoxCountryRegion = "#locationComboBox"
    basic_setup_country_region = "#countryList"
    country_region_vietnampopup_list = {
        FaxModemType.crawdad_aabrazil.value:"#countryValueUnitedStatespopupList",   # fax_mode = "2 - APJ"
        FaxModemType.dungeness_worldwide_modem.value:"#countryValueUnitedArabEmiratespopupList",   # fax_mode = "3 - World wide"
        FaxModemType.dungeness_bbu_modem.value:"#countryValueVietnampopupList" } # fax_mode = "NONE"
    combo_box_list_country_region = "#locationComboBoxpopupList"
    title_big_item = "#titleBigItem"
    title_small_item = "#titleSmallItem"
    title_object = "#titleObject"

    # country list
    country_region_none = "#settingsList_countryValueNone"
    country_region_id = "#settingsList_countryValueIndonesia"
    country_region_hk = "#settingsList_countryValueHongKongSAR"
    country_region_kr = "#settingsList_countryValueSouthKorea"
    country_region_my = "#settingsList_countryValueMalaysia"
    country_region_ph = "#settingsList_countryValuePhilippines"
    country_region_sg = "#settingsList_countryValueSingapore"
    country_region_th = "#settingsList_countryValueThailand"
    country_region_vn = "#settingsList_countryValueVietnam"
    country_region_lk = "#settingsList_countryValueSriLanka"
    country_region_ar = "#settingsList_countryValueArgentina"
    country_region_au = "#settingsList_countryValueAustralia"
    country_region_at = "#settingsList_countryValueAustria"
    country_region_by = "#settingsList_countryValueBelarus"
    country_region_be = "#settingsList_countryValueBelgium"
    country_region_br = "#settingsList_countryValueBrazil"
    country_region_bg = "#settingsList_countryValueBulgaria"
    country_region_ca = "#settingsList_countryValueCanada"
    country_region_cl = "#settingsList_countryValueChile"
    country_region_cn = "#settingsList_countryValueChina"
    country_region_hr = "#settingsList_countryValueCroatia"
    country_region_cz = "#settingsList_countryValueCzechRepublic"
    country_region_dk = "#settingsList_countryValueDenmark"
    country_region_ee = "#settingsList_countryValueEstonia"
    country_region_fi = "#settingsList_countryValueFinland"
    country_region_fr = "#settingsList_countryValueFrance"
    country_region_de = "#settingsList_countryValueGermany"
    country_region_gr = "#settingsList_countryValueGreece"
    country_region_hu = "#settingsList_countryValueHungary"
    country_region_is = "#settingsList_countryValueIceland"
    country_region_in = "#settingsList_countryValueIndia"
    country_region_ie = "#settingsList_countryValueIreland"
    country_region_il = "#settingsList_countryValueIsrael"
    country_region_it = "#settingsList_countryValueItaly"
    country_region_jp = "#settingsList_countryValueJapan"
    country_region_lv = "#settingsList_countryValueLatvia"
    country_region_li = "#settingsList_countryValueLiechtenstein"
    country_region_lt = "#settingsList_countryValueLithuania"
    country_region_lu = "#settingsList_countryValueLuxembourg"
    country_region_mx = "#settingsList_countryValueMexico"
    country_region_ma = "#settingsList_countryValueMorocco"
    country_region_nl = "#settingsList_countryValueNetherlands"
    country_region_nz = "#settingsList_countryValueNewZealand"
    country_region_no = "#settingsList_countryValueNorway"
    country_region_pk = "#settingsList_countryValuePakistan"
    country_region_pe = "#settingsList_countryValuePeru"
    country_region_pl = "#settingsList_countryValuePoland"
    country_region_pt = "#settingsList_countryValuePortugal"
    country_region_ro = "#settingsList_countryValueRomania"
    country_region_ru = "#settingsList_countryValueRussia"
    country_region_sk = "#settingsList_countryValueSlovakia"
    country_region_si = "#settingsList_countryValueSlovenia"
    country_region_za = "#settingsList_countryValueSouthAfrica"
    country_region_es = "#settingsList_countryValueSpain"
    country_region_se = "#settingsList_countryValueSweden"
    country_region_ch = "#settingsList_countryValueSwitzerland"
    country_region_tw = "#settingsList_countryValueTaiwanRegion"
    country_region_tr = "#settingsList_countryValueTurkey"
    country_region_ua = "#settingsList_countryValueUkraine"
    country_region_gb = "#settingsList_countryValueUnitedKingdom"
    country_region_us = "#settingsList_countryValueUnitedStates"
    # country_region_usa = ""   USA has no corresponding targeting
    
    countryRegion_dict = {
        "HK" : "#ComboBoxOPtionsHK",
        "Indonesia" : "#ComboBoxOPtionsHK"
    }

    country_region_popup_list = {
        FaxModemType.crawdad_aabrazil.value:"#countryValueUnitedStates",   # fax_mode = "2 - APJ"
        FaxModemType.dungeness_worldwide_modem.value:"#countryValueUnitedArabEmirates",   # fax_mode = "3 - World wide"
        FaxModemType.dungeness_bbu_modem.value:"#countryValueVietnam" } # fax_mode = "NONE"
        
    fax_item_dict = {
        "#faxSettingsSettingsButton": 1
        
    }

    fax_countrylist_scrollbar = {
        FaxModemType.crawdad_aabrazil.value:"#countryValueUnitedStatesScrollBar",   # fax_mode = "2 - APJ"
        FaxModemType.dungeness_worldwide_modem.value:"#countryValueUnitedArabEmiratesScrollBar",   # fax_mode = "3 - World wide"
        FaxModemType.dungeness_bbu_modem.value:"#countryValueVietnamScrollBar" } # fax_mode = "NONE"
    # Add Page
    view_add_page_screen = "#flatbedAddPage"
    button_finish_on_add_page = "#finish"
    button_add_more_on_add_page = "#addMoreButton"
    button_cancel_on_add_page = "#cancel"
    add_page_title_text_view = "#flatbedAddPage #TitleText #titleObject"
    add_page_description_text_view = "#flatbedAddPage #alertDetailDescription #contentItem"

    # Output Tray Closed
    view_output_tray_closed = "#trayOpen"
    output_tray_closed_title = "#trayOpen #TitleText #TitleTextHeaderView"
    output_tray_closed_body = "#trayOpen #alertDetailDescription #contentItem"
    output_tray_closed_footer_ok = "#trayOpen #AlertFooter #ButtonControl #ContentItem"

    spice_view = "#SpiceView"
    spice_text_view = "SpiceText[visible=true]"
    checkbox_text = "#CheckboxText" 
    content_item = "#contentItem"
    content_item_text = "#ContentItemText"

    # cstring id
    button_fax_setup_answering_machine_yes_cstring_id = "cYes"
    button_fax_setup_answering_machine_no_cstring_id = "cNo"

    #resolution dict
    resolution_dict = {
        "fine": ["cFaxResolutionFine", combo_resolution_option_Fine],
        "superfine": ["cSuperfine",combo_resolution_option_Superfine],
        "standard": ["cStandard", combo_resolution_option_Standrad]
    }

    #content type dict
    content_type_dict = {
        "mixed": ["cMixed", combo_contentTYpe_option_mixed],
        "photograph": ["cPhotographQuickSet",combo_contentTYpe_option_photograph],
        "text": ["cText", combo_contentTYpe_option_text],
        "automatic": ["cAutomatic", combo_contentTYpe_option_automatic],
        "image": ["cImage", combo_contentTYpe_option_image]
    }

    content_orientation_dict = {
        "portrait": ["cPortrait", orientation_portrait_option],
        "landscape": ["cLandscape",orientation_landscape_option]
    }

    alert_description = "#alertDetailDescription #contentItem"
    ok_button_alert_description = "#AlertFooter #OkButton"

    troubleshooting_fax_view_screen ="#clearFaxLogMemoryView"
    troubleshooting_fax_clearlogs_clear_button = "#clearButton"
    troubleshooting_fax_toastwindow = "#ToastWindowToastStackView"
    troubleshooting_fax_toastinfo = "#infoTextToastMessage"

#Schedule Fax
    fax_schedule_view="#scheduleFaxView"
    fax_schedule_screen_view="#SpiceHeaderVar2HeaderView"
    fax_send_now_set_min_value="#Minute"
    fax_send_now_set_hr_value="#Hour"
    fax_send_now_text_input = "#SpinBoxTextInput"
    fax_schedule_done="#scheduleLaterDoneButton"
    fax_schedule_reset="#scheduleLaterResetButton"

    fax_send_cancel="#cancelButton"

# Color Fax option
    fax_colormodesettingscomboBox_row = "#scan_colorModeSettingsComboBox"
    fax_scan_colormodecomboBox_item  ="#scan_colorModeComboBox"
    fax_options_grayscale = "#scan_colorModeComboBoxpopupList #ComboBoxOptionsgrayscale"
    fax_options_color = "#scan_colorModeComboBoxpopupList #ComboBoxOptionscolor"
    fax_color_mode_alert = "#faxColorModeAlert"
    ok_button_color_mode_alert = "#AlertFooter #faxAlertFooterOkBtn"
    send_button_color_mode_alert = "#AlertFooter #faxAlertFooterSendBtn"
    button_color_cancel_mode_alert = "#AlertFooter #faxAlertFooterCancelBtn"
# Fax alert
    alert_content = "#faxColorModeAlert #alertDetailDescription"
    color_fax_not_supported = "#faxColorModeAlert"
    color_fax_not_supported_body = "#alertDetailDescription #contentItem"
    ok_button_on_color_fax_not_supported = "#colorFaxNotSupportedOkButton"
    fax_send_state_window = "#faxSendStateWindow"

    footer_view = "#FooterView"

    fax_stored_item = "#StoredFaxes"

#Hook Operations
    go_on_hook = "#goOnHookButtonModel"
    go_off_hook = "#goOffHookButtonModel"
    refresh_button = "#doneButton"
    backbutton = "#BackButton"

#output Bin selection
    output_bin_selection = "#outputBinMenuSelectionList"
    output_bin1_selected = "#tray_dash_1outputBin"
    output_bin2_selected = "#tray_dash_2outputBin"
    output_bin3_selected = "#tray_dash_3outputBin"
    output_bin_automatic_selected = "#auto_outputBin"
    outputBinSettingsTextImage = "#outputBinSettingsTextImage"

#Generate Random Data
    radioButton_v21300 = "#v21_300"
    radioButton_v1714400 = "#v17_14400"
    radioButton_v1712000 = "#v17_12000"
    radioButton_v299600 = "#v29_9600"
    radioButton_v297200 = "#v29_7200"
    radioButton_v274800 = "#v27_4800"
    radioButton_v272400 = "#v27_2400"
    radioButton_v3433600 = "#v34_33600"
    radioButton_v3431200 = "#v34_31200"
    radioButton_v3428800 = "#v34_28800"
    radioButton_v3426400 = "#v34_26400"
    radioButton_v3424000 = "#v34_24000"
    radioButton_v3421600 = "#v34_21600"
    radioButton_v3419200 = "#v34_19200"
    radioButton_v3416800 = "#v34_16800"
    radioButton_v3414400 = "#v34_14400"
    radioButton_v3412000 = "#v34_12000"
    radioButton_v349600 = "#v34_9600"
    radioButton_v347200 = "#v34_7200"
    radioButton_v344800 = "#v34_4800"
    radioButton_v342400 = "#v34_2400"
    radioButton_v343429 = "#v34_3429"
    radioButton_v343200H = "#v34_3200H"
    radioButton_v343200L = "#v34_3200L"
    radioButton_v343000H = "#v34_3000H"
    radioButton_v343000L = "#v34_3000L"
    radioButton_v342800H = "#v34_2800H"
    radioButton_v342800L = "#v34_2800L"
    radioButton_v342743H = "#v34_2743H"
    radioButton_v342743L = "#v34_2743L"
    radioButton_v342400H = "#v34_2400H"
    radioButton_v342400L = "#v34_2400L"
    startstopbutton = "#startStopButton"
    donebutton = "#DoneButton"
    view_service_faxdiagnostics_generaterandomdata = "#generateRandomDataView"
    scrollBar_generateRandomData = "#generateRandomDataViewScrollBar"

#Generate Dialing Tones/Pulses
    diagnostic_dialing_scrollbar = "#generatePulseToneBurstViewScrollBar"
    diagnostic_dialing_pulseradiobutton ="#pulseBurstButton"
    diagnostic_dialing_toneradiobutton = "#toneBurstButton"
    diagnostic_dialing_continuoustoneradiobutton = "#continuousToneButton"
    diagnostic_dialing_lastdigittextbox = "#lastDigitsTextObj"
    diagnostic_dialing_startbutton = "#startStopButton"
    diagnostic_dialing_donebutton = "#DoneButton"
    diagnostic_dialing_lastdigitcombobox ="#SettingsComboBox"
    diagnostic_dialing_lastdigitscrollbar ="#comboBoxScrollBar"
    diagnostic_dialing_lastdigitcombopopoup = "#SettingsSpiceComboBoxpopup"
    lastdigit_dialing_optionStar = "*"
    lastdigit_dialing_optionHash = "#"
    lastdigit_dialing_optionA = "A"
    lastdigit_dialing_optionB = "B"
    lastdigit_dialing_optionC = "C"
    lastdigit_dialing_optionD = "D"
    lastdigit_dialing_option0 = "0"
    lastdigit_dialing_option1 = "1"
    lastdigit_dialing_option2 = "2"
    lastdigit_dialing_option3 = "3"
    lastdigit_dialing_option4 = "4"
    lastdigit_dialing_option5 = "5"
    lastdigit_dialing_option6 = "6"
    lastdigit_dialing_option7 = "7"
    lastdigit_dialing_option8 = "8"
    lastdigit_dialing_option9 = "9"
    view_service_faxdiagnostics_generatePulseToneBurstView = "#generatePulseToneBurstView"
    ok_enterKeyPositiveIntegerKeypad = "#enterKeyPositiveIntegerKeypad"

#Generate/Dial Phone Number
    tone_button = "#faxDialTypeToneButton"
    pulse_button = "#faxDialTypePulseButton"
    #fax_number_text = "#textFieldContainer"
    fax_number_text = "#phoneNoTextField"
    diagnostic_phonenumber_dailbutton = "#dialButton"
    diagnostic_phonenumber_donebutton = "#DoneButton"

#Generate Single Modem Tone
    tone1100 = "#tone1100"
    tone1300 = "#tone1300"
    tone1800 = "#tone1800"
    tone2100 = "#tone2100"
    generate_start_button = "#startStop"
    single_modem_tone_donebutton = "#DoneButton"
    view_service_faxdiagnostics_singlemodemtone = "#generateSingleModemTone"
    scrollbar_single_modem_tone = "#generateSingleModemToneScrollBar"

#Fax Transmit Signal Loss
    up_button = "#upBtn"
    signal_level = "#signalLevel"
    spin_box_row = "#spinbox"
    proceed_button = "#proceedButton"

#V.29 Speed Selection
    v29speed_9600 = "#v29Speed9600Button"
    v29speed_7200 = "#v29Speed7200Button"

#Ring Settings
    off_button = "#offButton"
    on_button = "#onButton"
    pbx_ringdetect_switch = "#pbxRingDetectSwitch"
    ring_frequency_up_button = "#upBtn"
    save_button = "#doneButton"
    ring_frequency_spinbox = "#ringFrequencySpinBox"
    ring_frequency_spinbox_text = "#SpinBoxTextInput"
    ring_interval_spinbox = "#ringIntervalSpinBox"
    ring_interval_spinbox_text = "#SpinBoxTextInput"
    view_ringSettingsScreen = "#ringSettings"
    scrollBar_ringSettings = "#ringSettingsScrollBar"

    pre_preview_content = "#contentText"
    pre_preview_layout = "#faxPrePreview" 

#Jam
    view_jam_screen = "#jamInScannerWindow"
    button_ok_scan_jam = "#okScanJam"
    
#runfaxtest - troubleshooting->diagnostic tests
    diagnostictests_menulist_view = "#diagnosticTests2MenuList"
    diagnostictests_menulist_scrollbar = "#diagnosticTests2MenuListScrollBar"
    menu_button_diagnostictests_runfaxtest = "#runFaxTest"
    button_runfaxtest_start = "#runFaxTestRow"
    # diagnostictests_exiting_maintenancemode = "#exitingMaintenanceMode"
    button_diagnostictests_exiting_maintenancemode_ok = "#maintenanceModeContinueButton"
    button_diagnostictests_exiting_maintenancemode_cancel = "#diagnosticProgressCancelButton"
    button_diagnostictests_back = "#BackButton"
    button_diagnostictests_home = "#HomeButton"
    
    # Workflow2 Specific ObjectID's
    home_swipe_view = "#homeScreenSwipeView"
    scanAutoDetectionPromptConfiguration = "#scanAutoDetectionPromptConfiguration"
    autoDetection_continueButton = "#continueButton"
    autoDetection_cancelButton = "#scanAutoDetectionPromptConfiguration #cancelButton"
    flatbedCancelPrompt = "#FlatbedCancelPrompt"
    flatbedCancelPromptYesButton = "#yesButton"
    flatbedCancelPromptNoButton = "#noButton"

    adfAddPagePrompt = "#adfAddPage"
    adfAddPage_start = "#AlertFooter #startButton"
    adfAddPage_cancel = "#AlertFooter #CancelButton"

    button_preview="#previewButton"
    button_preview_large="#previewButtonLargeScreen"
    button_collapse_secondarypanel="#_CollapseButton"
    button_expand_secondarypanel="#FooterView #FooterViewRight #_ExpandButton"
    preview_panel="#itempreview"
    fitpage_layout="#FitPage"
    first_preview_image="#image_0"
    preview_cancel_job_warning_prompt = "#CancelJobWarningPrompt"
    preview_cancel_job_warning_prompt_primary_button = preview_cancel_job_warning_prompt + " #cancelJobWarningPrimaryButton"
    preview_cancel_job_warning_prompt_secondary_button = preview_cancel_job_warning_prompt + " #cancelJobWarningSecondaryButton"
    preview_image_without_index = "#image_"
    previewWindow='#previewTemplate'
    preview_back_button="#HeaderViewLeft #SpiceBreadcrumb #BreadcrumbView #BackButton"
    preview_header = "#previewHeader"
    preview_header_moreOptions = "#moreOptions"
    zoomOut_button = "#zoomOutButton"
    zoomIn_button = "#zoomInButton"
    fitHeightButton = "#fitHeightButton"
    fitWidthButton = "#fitWidthButton"
    prepreview_enabled_string_id = "cConfigurePreviewSettings"
    prepreview_layout ="#prePreview"