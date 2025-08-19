class SubstrateLibraryWorkflowObjectIds:

    # VIEWS/SCREENS

    # installed substrates
    view_substrateLibrary = "#mediaLibraryLayout"
    view_installedSubstrates = "#installedSubstratesLayout"
    view_mediaLibraryLayoutHeader = "#mediaLibraryAppHeader"
    view_mediaLibraryLayoutFooter = "#mediaLibraryTabsFooter"
    view_category = "#installedSubstratesLayoutlist"                         # for all types of papers is the same view name
    view_substrate = "#mediaModesLayoutListView"
    view_clone_substrate = "#cloneSubstrateInsertName"
    view_clone_progress = "#cloneSubstrateProgress"
    view_clone_success = "#cloneSubstrateSuccess"
    view_rename_substrate = "#renameSubstrateInsertName"
    view_rename_progress = "#renameSubstrateProgress"
    view_rename_success = "#renameSubstrateSuccess"
    view_delete_substrate = "#deleteSubstrateConfirmation"
    view_delete_progress = "#deleteSubstrateProgress"
    view_delete_success = "#deleteSubstrateSuccess"
    view_edit_loadingData_progress = "#editMediaModeLoadingDataProgress"
    view_edit_printmode = "#editMediaModeEditValuesScreen"
    view_edit_printmode_progress = "#editMediaModeProgress"
    view_edit_printmode_success = "#editMediaModeSuccess"
    view_delete_mediamode_confirmation = "#deleteMediaModeConfirmation"
    view_delete_mediamode_progress = "#deleteMediaModeProgress"
    view_delete_mediamode_success = "#deleteMediaModeSuccess"

    #add new print mode
    view_loadingData_progress = "#addMediaModeLoadingDataProgress"
    view_add_printmode = "#addMediaModeEditValuesScreen"
    view_add_printmode_progress = "#addMediaModeProgress"
    view_add_printmode_success = "#addMediaModeSuccess"

    #add new substrate
    button_add = "#addNewMediaButton"
    add_choose_substrate_name_next_button = "#chooseSubstrateNameNextButton"
    add_choose_substrate_category_next_button = "#chooseSubstrateCategoryNextButton"
    add_choose_base_substrate_next_button = "#chooseBaseSubstrateNextButton"

    view_choose_substrate_name = "#addSubstrateChooseSubstrateNameScreen"
    view_choose_category = "#addSubstrateChooseCategoryScreen"
    view_choose_base_substrate = "#addSubstrateChooseBaseSubstrateScreen"
    add_substrate_view_model = "#substrateNameTextFieldNode"
    add_substrate_text_field = "#substrateNameTextFieldModel"
    view_add_media_mode = "#addSubstrateAddMediaModeEditValuesScreen"
    view_add_media_mode_progress = "#addSubstrateAddMediaModeProgress"
    view_add_substrate_progress = "#addSubstrateProgress"
    view_print_test_plot = "#testPlotNotDoneAdviceScreen"
    view_success_screen = "#addSubstrateSuccess"
    media_mode_text_field = "#mediaModeNameTextFieldModel"
    color_mode_box = "#mediaModeColorModeRow #SettingsSpiceComboBox"
    color_mode_box_popup = "#mediaModeColorModeRow #SettingsSpiceComboBox #SettingsSpiceComboBoxpopupList"
    color_mode_cmykLiteS = "#colorMode_cmykLiteSRadioButtonModel"
    color_mode_cmyk = "#colorMode_cmykLiteS"
    number_of_passes_box = "#mediaModePassesRow #SettingsSpiceComboBox"
    passes_selection = "#passes_{}"
    ink_density_box = "#mediaModeInkDensityRow #SettingsSpiceComboBox"
    ink_density_selection = "#inkDensity_{}"
    done_media_mode_button = "#userDoneButton"
    cancel_print_test_plot_button = "#userContinueButton"
    button_textile_add = "#textileRadioButtonModel"
    user_confirm_button = "#userConfirmButton"
    substrate_name_alert = "#substrateNameTextFieldModel #HelperMessageContentItem #HelperText"

    #Calibrations
    calibrations_layout = "#calibrationsLayout"
    skip_calibration_button = "#userSkipCalibrationsButton"
    view_routines_not_done_advice = "#calibrationNotDoneAdviceScreen"
    continue_anyway_routine_button = "#userContinueAnywayButton"
    routines_controller = "#routinesController"

    # gaia
    view_gaia_packages = "#deploymentsLayout"
    view_gaia_deployments_list = "#deploymentsContainerList"
    view_gaia_deployments_cards_list = "#deploymentsContainerCard"
    view_gaia_device_not_paired = "#printerNotPairedScreen"
    view_gaia_devoce_not_conencted = "#noInternetConnectionScreen"
    view_gaia_no_deployments = "#noDeploymentsScreen"
    view_gaia_deployment_element_in_list = "#deployment_{}"
    view_gaia_deployment_detail = "#deploymentDetail"

    # gaia/install
    view_install_confirm_append = "#confirmAppendDialog"
    view_install_confirm_replace = "#confirmReplaceDialog"
    view_install_backup_progress = "#backupProgressWizard"
    view_install_download_progress = "#downloadProgressWizard"
    view_install_install_progress = "#installProgressWizard"
    view_install_backup_failed = "#backupFailedDialog"
    view_install_failed = "#installFailure"
    view_install_successfull = "#installSuccessWizard"

    # gaia/backup
    view_backup_device_not_paired = "#notPairedDialog"
    view_backup_device_not_connected = "#noInternetDialog"
    view_backup_no_custom_medias = "#noCustomMediasDialog"
    view_backup_insert_name = "#backupCloudDialog"
    view_backup_another_in_progress = "#otherInProgressDialog"

    # LAYOUTS

    # WIDGETS ON SCREEN: Buttons, textboxes, menu icons, tabs etc.
    home_button_substrate_library = "#3e7cc42a-d7ff-11eb-9ddc-d3f9425e6ff9"
    tab_installed_substrates = "#installedSubstratesTabModel"
    tab_gaia_packages = "#deploymentsTab"
    button_category_self_adhesive_vinyl = "#0"
    button_category_banner = "#2"
    button_category_blueprint = "#4"
    button_category_custom_paper = "#6"
    button_category_film_paper = "#7"
    button_category_heat_transfer_paper = "#8"
    button_category_plain_paper = "#9"
    button_category_textile_paper = "#12"
    category_adhesive ="adhesive"
    category_backlit ="backlit"
    category_bannerAndSign ="bannerAndSign"
    category_bondAndCoated ="bondAndCoated"
    category_blueprint ="blueprint"
    category_canvas ="canvas"
    category_custom ="custom"
    category_film ="film"
    category_heatTransfer ="heatTransfer"
    category_plain ="plain"
    category_photo ="photo"
    category_technical ="technical"
    category_textile ="textile"
    category_wallcovering ="wallcovering"
    category_unknown ="unknown"
    button_generic_self_adhesive_vinyl = "#150100"
    button_clone = "#mainActionCloneButton"
    txt_clone_insert_name = "#cloneSubstrateInsertNameTextField"
    button_clone_ok = "#userOkButton"
    button_ok = "#okButton"
    button_no = "#noButton"
    button_cancel = "#cancelButton"
    button_done = "#userDoneButton"
    button_install = "#installButton"
    button_retry = "#retryButton"
    button_user_cancel = "#userCancelButton"
    continue_button = "#userContinueButton"
    print_test_button = "#userPrintTestButton"
    button_backup = "#backupPackagesButton"
    button_home = "#HomeButton"
    button_back = "#BackButton"
    button_rename = "#renameDetailsButton"
    button_delete = "#deleteDetailsButton"
    rename_text_bar = "#renameSubstrateInsertNameTextField"
    button_delete_ok = "#userDeleteButton"
    button_more_options = "#moreOptionsDetailsButton"
    button_options_rename = "#renameButton"
    button_substrate_options = "#moreOptionsButton"
    # edit printmode
    button_edit_printmode = "#editMediaModeMoreOptionsButtonModel"
    button_mediaMode_options = "#editMediaModeButtonModel"
    txt_printmode_name = "#mediaModeNameTextFieldModel"
    curing_temperature_row = "#mediaModeCuringTemperatureRow"
    curing_temperature_model = "#mediaModeCuringTemperatureModelSettingDetailsScreen"
    curing_temperature_spinbox = "#mediaModeCuringTemperatureModelSpinBoxModel"
    curing_temperature_backButton = "#mediaModeSettingDetailsScreenHeader #mediaModeSettingDetailsScreenHeaderHeaderView #SpiceBreadcrumb #BreadcrumbView #BackButton"
    curing_temperature_value = "#mediaModeCuringTemperatureRow_2infoBlockRow SpiceText[visible=true]"
    vacuum_row = "#mediaModeVacuumRow"
    vacuum_model = "#mediaModeVacuumModelSettingDetailsScreen"
    vacuum_spinbox = "#mediaModeVacuumModelSpinBoxModel"
    vacuum_value = "#mediaModeVacuumRow_2infoBlockRow SpiceText[visible=true]"
    spinbox_button_up = "#upButtonContainer"
    spinbox_button_down = "#downButtonContainer"
    more_settings_row = "#mediaModeMoreSettingsRow"
    distance_job_row = "#mediaModeDistanceBetweenJobsRow"
    distance_job_model = "#mediaModeDistanceBetweenJobsModelSettingDetailsScreen"
    distance_job_spinbox = "#mediaModeDistanceBetweenJobsModelSpinBoxModel"
    distance_job_backButton = "#mediaModeSettingDetailsScreenHeader #mediaModeSettingDetailsScreenHeaderHeaderView #SpiceBreadcrumb #BreadcrumbView #BackButton"
    more_settings_header = "#moreSettingsHeader"
    advance_setting_row = "#mediaModeAdvanceSettingsRow"
    advance_panel = "#advancedSettingsPanelModelListLayout"
    blooming_level_row = "#mediaModeBloomingLevelRow"
    blooming_level_first_block = "#mediaModeBloomingLevelRow_firstinfoBlockRow"
    blooming_level_second_block_value = "#mediaModeBloomingLevelRow_2infoBlockRow #secondInfoBlockModelChevronRight SpiceText[visible=true]"
    blooming_level_model = "#mediaModeBloomingLevelModelSettingDetailsScreen"
    blooming_level_ComboBox = "#mediaModeBloomingLevelModelSettingDetailsScreenlist1 #SettingsSpiceComboBox"
    blooming_level_ComboBox_popup = "#mediaModeBloomingLevelRow_firstinfoBlockRow #SettingsSpiceComboBox #SettingsSpiceComboBoxpopupList"
    blooming_level_backButton = "#mediaModeBloomingLevelModelSettingDetailsScreenlist1 #mediaModeSettingDetailsScreenHeader #mediaModeSettingDetailsScreenHeaderHeaderView #SpiceBreadcrumb #BreadcrumbView #BackButton"
    blooming_level_2 = "#bloomingLevel_2"
    blooming_level_3 = "#bloomingLevel_3"
    advance_factor_row = "#mediaModeAdvanceFactorRow"
    advance_factor_row_value = "#mediaModeAdvanceFactorRow_2infoBlockRow SpiceText[visible=true]"
    advance_factor_model = "#mediaModeAdvanceFactorModelSettingDetailsScreen"
    advance_factor_switch = "#mediaModeAdvanceFactorModelSwitchModel"
    speed_print_mode_options_button = "#Speed_primaryButton"
    edit_media_mode_scroll_bar = "#editMediaModeEditValuesScreenlist1ScrollBar"       # Scroll bar in edit media mode screen
    edit_media_mode_advance_scroll_bar = "#editMediaModeEditValuesScreenlistScrollBar"

    # delete mediamode
    button_delete_mediamode = "#deleteMediaModeMoreOptionsButtonModel"
    # add new printmode
    button_add_printmode = "#mainActionAddMediaModeButton"                # button on Custom Substrate view
    # general
    button_menu_on_homescreen = "#floatingDockButton"                       # Menu Button/icon on HOME screen
    scrollbar_main_menu = "#landingPageMenuAppListScrollBar"                        # Scrollbar in main menu
    scrollbar_installed_substrates_layout_categories = "#installedSubstratesLayoutlist1ScrollBar" # Scrollbar in installed substrates layout categories
    scrollbar_installed_substrates_layout_substrates = "#installedSubstratesLayoutlistScrollBar" # Scrollbar in installed substrates layout substrates
    scrollbar_mediaModes_layout = "#mediaModesLayoutListViewScrollBar" # Scrollbar in mediaModes layout
    button_substratelibrary_app = "#3e7cc42a-d7ff-11eb-9ddc-d3f9425e6ff9MenuApp"    # Button in main menu
    add_media_mode_scroll_bar = "#addMediaModeEditValuesScreenlist1ScrollBar"       # Scroll bar in add media mode screen
    add_media_mode_scroll_bar_2 = "#addMediaModeEditValuesScreenlistScrollBar"       # Scroll bar in add media mode screen
    choose_category_sroll_bar = "#addSubstrateChooseCategoryScreenlist1ScrollBar"               # Scroll bar in category screen

    # gaia
    toast_message_text = "#infoTextToastMessage"
    backup_name_text_field = "#backupCloudNameField"
    deployment_detail_status_box = "#deploymentDetail #rowBlockC #statusBoxBlockC"
    deployment_detail_status_box_text = "#deploymentDetail #rowBlockC #statusBoxBlockC #StatusText"
    deployment_detail_text = "#deploymentDetailHeader #leftBlockObject #titleObject"
    deployment_detail_included_media_text = "#deploymentDetailContentIncludedMediaRow SpiceText[visible=true]"
    deployment_detail_scroll = "#DetailInfoverticalLayoutScrollBar"
    deployment_element_text = "#deployment_{} #infoBlockinfoBlockRow SpiceText[visible=true]"
    dpeloyment_element_icon = "#deployment_{} #infoBlockinfoBlockRow #imageItem"
    deployment_element_install_button = "#deployment_{}_primaryButton"

    # Mismatch screen
    media_mismatch_window = "#mediaMismatchSizeFlow"
    mismatch_options_button = "#CollapseButton"
    print_anyway_button = "#continueBtn"

    # Clone failure (limit reached)
    clone_substrate_title = "#cloneSubstrateStorageError #TitleTextHeaderView #titleObject"
    substrate_not_added   = "#cloneSubstrateStorageError #LayoutHorizontalIconsGrid #alertDetailDescription #contentItem"
    memory_full           = "#cloneSubstrateStorageError #LayoutHorizontalIconsGrid #alertDetailDescription #contentItem"
    buttonOKCloneFailure  = "#cloneSubstrateStorageError #AlertFooter #userOkButton"

    # Add printmode failure (limit reached)
    add_printmode_title         = "#addMediaModeMaxNumberError #TitleTextHeaderView #titleObject"
    media_mode_not_added        = "#addMediaModeMaxNumberError #LayoutHorizontalIconsGrid #alertDetailDescription #contentItem"
    buttonOkAddMediaModeFailure = "#addMediaModeMaxNumberError #AlertFooter #userOkButton"