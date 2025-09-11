from typing import  Final, Callable
from dunetuf.ui.new.shared.locator_base import Locator, CSS, OID



class CopyLoc:

    # ------------------------------- Generic / Common ------------------------------ #
    mouse_area_locator = Locator("css", " MouseArea")

    # ------------------------------- Buttons / Actions ------------------------------- #
    button_copy_app: Final = CSS("#cedab422-33b3-4638-b6a1-604e54525215")
    button_id_card_copy: Final = CSS("#c74293eb-04c1-4dff-b469-1c0e99fdbe8b")
    button_start_copy: Final = CSS("#mainActionButtonOfDetailPanel")
    button_copy_more_options: Final = CSS("#DetailPanelverticalLayout #FooterViewRight #optionsDetailPanelButton")
    button_done: Final = CSS("#mainActionButtonOfDetailPanel")
    button_copy: Final = CSS("#mainActionButtonOfDetailPanel")
    button_eject_main: Final = CSS("#ejectMainPanelButton")
    button_eject_detail_panel: Final = CSS("#ejectDetailPanelButton")
    button_ok: Final = CSS("#okButton")
    start_button_text: Final = CSS("SpiceText:contains('Start')")  # si tu UDW soporta :contains

    # ------------------------------- Views / Panels --------------------------------- #
    view_copy_option_list: Final = CSS("copySettingsPage_list1 #copySettingsPage_list1")
    view_copy_screen: Final = CSS("#copyLandingView")
    view_ui_main_app: Final = CSS("#HomeScreenView")
    detail_panel_layout: Final = CSS("#DetailPanelverticalLayout")
    vertical_layout_scrollbar: Final = CSS("#DetailPanelverticalLayoutScrollBar")

    # ------------------------------- Number of copies -------------------------------- #
    spinbox_copies: Final = CSS("#copy_numberOfCopiesMenuSpinBox")
    row_spinbox_copies: Final = CSS("#copy_numberOfCopiesSettingsSpinBox")
    spinbox_copies_plus: Final = CSS("#copy_numberOfCopiesMenuSpinBox #upBtn")
    spinbox_copies_minus: Final = CSS("#copy_numberOfCopiesMenuSpinBox #downBtn")
    spinbox_copies_text: Final = CSS("#SpinBoxTextInput")
    spinbox_copies_text_mouse_area: Final = CSS("#SpinBoxTextFieldMouseArea")

    # ------------------------------- Quality ---------------------------------------- #
    row_combo_quality: Final = CSS("#copy_qualitySettingsComboBox")
    combo_quality: Final = CSS("#copy_qualityComboBox")
    view_quality_list: Final = CSS("#copy_qualityComboBoxpopupList")
    opt_quality_standard: Final = CSS("#ComboBoxOptionsnormal")
    opt_quality_draft: Final = CSS("#ComboBoxOptionsdraft")
    opt_quality_best: Final = CSS("#ComboBoxOptionsbest")

    # ------------------------------- Pages per sheet -------------------------------- #
    row_combo_pages_per_sheet: Final = CSS("#copy_pagesPerSheetSettingsComboBox")
    combo_pages_per_sheet: Final = CSS("#copy_pagesPerSheetComboBox")
    view_pages_per_sheet_list: Final = CSS("#copy_pagesPerSheetComboBoxpopupList")
    view_pages_per_sheet_popup: Final = CSS("#copy_pagesPerSheetComboBoxpopup")
    opt_pages_1: Final = CSS("#ComboBoxOptionsoneUp")
    opt_pages_2: Final = CSS("#ComboBoxOptionstwoUp")
    opt_pages_4_right_then_down: Final = CSS("#ComboBoxOptionsfourRightThenDown")
    opt_pages_4_down_then_right: Final = CSS("#ComboBoxOptionsfourDownThenRight")
    list_pages_per_sheet: Final = CSS("#copySettingPagesPerSheet")
    list_view_pages_per_sheet: Final = CSS("#copy_pagesPerSheetView")
    list_pages_per_sheet_value: Final = CSS("#copySettingPagesPerSheet_2infoBlockRow")
    check_add_page_borders: Final = CSS("#CheckBoxOptionsAddPageBorders")
    row_add_page_borders: Final = CSS("#AddPageBorders")
    pages_per_sheet_scrollbar: Final = CSS("#copy_pagesPerSheetViewScrollBar")

    # ------------------------------- Sides (duplex) --------------------------------- #
    row_combo_sides: Final = CSS("#copy_sidesMenuComboBox")
    combo_sides: Final = CSS("#SettingsSpiceComboBox")
    view_sides_popup_list: Final = CSS("#SettingsSpiceComboBoxpopupList")
    view_sides_popup: Final = CSS("#SettingsSpiceComboBoxpopup")
    opt_sides_1to1: Final = CSS("#Copy1to1Sided")
    opt_sides_1to2: Final = CSS("#Copy1to2Sided")
    opt_sides_2to1: Final = CSS("#Copy2to1Sided")
    opt_sides_2to2: Final = CSS("#Copy2to2Sided")

    opt_sides_1to1_radio: Final = CSS("#Copy1to1SidedRadioButtonModel")
    opt_sides_1to2_radio: Final = CSS("#Copy1to2SidedRadioButtonModel")
    opt_sides_2to1_radio: Final = CSS("#Copy2to1SidedRadioButtonModel")
    opt_sides_2to2_radio: Final = CSS("#Copy2to2SidedRadioButtonModel")

    # ------ Duplex: flujo "add page" (tus 3 de ejemplo) ------
    duplex_add_more: Final = CSS("#addMoreButton")
    duplex_finish:   Final = CSS("#finish")
    duplex_cancel:   Final = CSS("#cancel")

    # ------------------------------- Scan mode -------------------------------------- #
    scan_mode_settings_option: Final = CSS("#scan_scanModeSettingsTextImage")
    row_scan_mode_settings_option: Final = CSS("#scan_scanModeSettingsTextImage_2infoBlockRow")
    view_scan_mode_list: Final = CSS("#copy_scanModeList")
    scan_mode_standard: Final = CSS("#scan_scanModestandard")
    scan_mode_job_build: Final = CSS("#scan_scanModejobBuild")
    scan_mode_id_card: Final = CSS("#scan_scanModeidCard")
    scan_mode_book_mode: Final = CSS("#scan_scanModebookMode")
    scan_mode_prompt_additional_pages: Final = CSS("#promptCheckBoxForAdditionalPages")
    scan_mode_prompt_scan_both_sides: Final = CSS("#promptCheckBoxForScanBothSides")
    scan_mode_scrollbar: Final = CSS("#copy_scanModeListScrollBar")

    # ------------------------------- Content type ----------------------------------- #
    combo_content_type_row: Final = CSS("#copySettingsPage_list1 #scan_contentTypeSettingsComboBox #scan_contentTypeComboBox")
    row_combo_content_type: Final = CSS("#scan_contentTypeSettingsComboBox")
    combo_content_type: Final = CSS("#scan_contentTypeComboBox")
    view_content_type_list: Final = CSS("#scan_contentTypeComboBoxpopupList")
    opt_content_text: Final = CSS("#ComboBoxOptionstext")
    opt_content_photograph: Final = CSS("#ComboBoxOptionsphoto")
    opt_content_lines: Final = CSS("#ComboBoxOptionslineDrawing")
    opt_content_image: Final = CSS("#ComboBoxOptionsimage")
    opt_content_mixed: Final = CSS("#ComboBoxOptionsmixed")

    # ------------------------------- Settings / Panels ------------------------------ #
    settings_open: Final = CSS("#optionsDetailPanelButton")
    settings_view: Final = CSS("#copySettingsView")

    # ------------------------------- Orientation ------------------------------------ #
    settings_orientation_combo: Final = CSS("#scan_contentOrientationComboBox")
    view_orientation_list: Final = CSS("#scan_contentOrientationComboBoxpopupList")
    opt_orientation_landscape: Final = CSS("#ComboBoxOptionslandscape")
    opt_orientation_portrait: Final = CSS("#ComboBoxOptionsportrait")

    # ------------------------------- Feature values (texto visible) ----------------- #
    value_color_mode: Final = CSS("#scan_colorModeComboBox SpiceText[visible=true]")
    value_quality: Final = CSS("#copy_qualityComboBox SpiceText[visible=true]")
    value_content_type: Final = CSS("#scan_contentTypeComboBox SpiceText[visible=true]")
    value_paper_source: Final = CSS("#copy_detailedPaperSourceComboBox SpiceText[visible=true]")
    value_number_of_copies: Final = CSS("#copy_numberOfCopiesMenuSpinBox #SpinBoxTextInput")

    # ------------------------------- Copy Margins ----------------------------------- #
    row_combo_margins: Final = CSS("#copy_marginsSettingsComboBox")
    combo_margins: Final = CSS("#copy_marginsComboBox")
    view_margins_list: Final = CSS("#copy_marginsComboBoxpopupList")
    opt_margins_clip: Final = CSS("#ComboBoxOptionsclipContents")
    opt_margins_add: Final = CSS("#ComboBoxOptionsaddToContents")

    # ------------------------------- Printing order --------------------------------- #
    row_combo_printing_order: Final = CSS("#copy_printingOrderSettingsComboBox")
    combo_printing_order: Final = CSS("#copy_printingOrderComboBox")
    view_printing_order_list: Final = CSS("#copy_printingOrderComboBoxpopupList")
    opt_order_first_on_top: Final = CSS("#ComboBoxOptionsfirstPageOnTop")
    opt_order_last_on_top: Final = CSS("#ComboBoxOptionslastPageOnTop")

    # ------------------------------- Add page (flatbed / prompts) ------------------- #
    flatbed_cancel_screen: Final = CSS("#FlatbedCancelPrompt")
    flatbed_two_sided_screen: Final = CSS("#flatbedAddPage")
    btn_add_page_add: Final = CSS("#addButton")
    btn_add_page_scan: Final = CSS("#scanButton")
    btn_add_page_done: Final = CSS("#doneButton")
    btn_add_page_cancel: Final = CSS("#addPagePromptView #cancelButton")
    btn_add_page_cancel_yes: Final = CSS("#yesButton")
    btn_add_page_cancel_no: Final = CSS("#noButton")
    view_add_page_prompt: Final = CSS("#addPagePromptView")
    add_page_prompt_scrollbar: Final = CSS("#addPageContentScrollBar")
    add_page_content: Final = CSS("#addPageContent")

    # ------------------------------- Color mode combo ------------------------------- #
    row_combo_color: Final = CSS("#scan_colorModeSettingsComboBox")
    combo_color: Final = CSS("#scan_colorModeComboBox")
    view_color_list: Final = CSS("#scan_colorModeComboBoxpopupList")
    opt_color_auto: Final = CSS("#ComboBoxOptionsautoDetect")
    opt_color_color: Final = CSS("#ComboBoxOptionscolor")
    opt_color_grayscale: Final = CSS("#ComboBoxOptionsgrayscale")
    opt_color_blackonly: Final = CSS("#ComboBoxOptionsmonochrome")

    # ------------------------------- Menú / navegación ------------------------------ #
    copy_landing_back: Final = CSS("#copyLandingView #BackButton")
    button_home: Final = CSS("#CopyAppApplicationStackView #HomeButton #ButtonControl")
    button_back: Final = CSS("#BackButton")
    button_close: Final = CSS("#closeButton")
    text_view: Final = CSS("SpiceText[visible=true]")
    options_scrollbar: Final = CSS("#copySettingsPage_list1ScrollBar")

    # ------------------------------- Paper Selection (combos) ----------------------- #
    list_paper_selection: Final = CSS("#copyPaperSelection")
    view_paper_selection: Final = CSS("#copy_paperSelectionMenuList")
    view_paper_selection_scrollbar: Final = CSS("#copy_paperSelectionMenuListScrollBar")

    # ------------------------------- Original Paper Type ---------------------------- #
    row_combo_original_paper_type: Final = CSS("#scan_originalMediaTypeSettingsComboBox")
    combo_original_paper_type: Final = CSS("#scan_originalMediaTypeComboBox")
    view_original_paper_type_list: Final = CSS("#scan_originalMediaTypeComboBoxpopupList")
    opt_original_paper_white: Final = CSS("#ComboBoxOptionswhitePaper")
    opt_original_paper_photo: Final = CSS("#ComboBoxOptionsphotoPaper")
    opt_original_paper_translucent: Final = CSS("#ComboBoxOptionstranslucentPaper")
    opt_original_paper_old_recycled: Final = CSS("#ComboBoxOptionsoldRecycledPaper")
    opt_original_paper_blueprints: Final = CSS("#ComboBoxOptionsblueprints")
    opt_original_paper_dark_blueprints: Final = CSS("#ComboBoxOptionsdarkBlueprints")

    # ------------------------------- Resolution ------------------------------------ #
    #TODO:
    combo_resolution_row: Final = CSS("#copySettingsPage_list1 #scan_resolutionSettingsComboBox #scan_resolutionComboBox")
    row_combo_resolution: Final = CSS("#scan_resolutionSettingsComboBox")
    combo_resolution: Final = CSS("#scan_resolutionComboBox")
    view_resolution_list: Final = CSS("#scan_resolutionComboBoxpopupList")
    opt_resolution_200: Final = CSS("#ComboBoxOptionse200Dpi")
    opt_resolution_300: Final = CSS("#ComboBoxOptionse300Dpi")
    opt_resolution_600: Final = CSS("#ComboBoxOptionse600Dpi")

    # ------------------------------- Invert Blueprints ------------------------------ #
    row_invert_blueprint_color: Final = CSS("#scan_invertBlueprintColorSettingsSwitch")
    toggle_invert_blueprint: Final = CSS("#scan_invertBlueprintColorsMenuSwitch")

    # ------------------------------- Number of Copies ------------------------ #
    spinbox_number_of_copies: Final = CSS("#copy_numberOfCopiesMenuSpinBox")
    row_spinbox_number_of_copies: Final = CSS("#copy_numberOfCopiesSettingsSpinBox")
    spinbox_number_of_copies_plus: Final = CSS("#copy_numberOfCopiesMenuSpinBox #upBtn")
    spinbox_number_of_copies_minus: Final = CSS("#copy_numberOfCopiesMenuSpinBox #downBtn")
    spinbox_number_of_copies_text_area: Final = CSS("#SpinBoxTextInput")

    # Original Paper Type (string IDs)
    sid_original_paper_white: Final = OID("cWhitePaper")
    sid_original_paper_photo: Final = OID("cPhotoPaper")
    sid_original_paper_translucent: Final = OID("cTranslucentPaper")
    sid_original_paper_old_recycled: Final = OID("cOldRecycledPaper")
    sid_original_paper_blueprints: Final = OID("cBlueprints")
    sid_original_paper_dark_blueprints: Final = OID("cDarkBlueprints")

    # Paper Source
    paper_source_row: Final = CSS("#copy_paperSourceSettingsComboBox")
    paper_source_combo: Final = CSS("#copy_paperSourceComboBox")
    paper_source_list: Final = CSS("#copy_paperSourceComboBoxpopupList")
    paper_source_auto: Final = CSS("#ComboBoxOptionsauto_")
    paper_source_roll1: Final = CSS("#ComboBoxOptionsroll_dash_1")
    paper_source_roll2: Final = CSS("#ComboBoxOptionsroll_dash_2")

    # Paper Tray (detalle)
    row_combo_paper_tray: Final = CSS("#copy_paperSourceSettingsComboBox")
    combo_paper_tray: Final = CSS("#copy_paperSourceComboBox")
    view_paper_tray_list: Final = CSS("#copy_paperSourceComboBoxpopupList")
    opt_tray1: Final = CSS("#ComboBoxOptionstray_dash_1")
    opt_tray2: Final = CSS("#ComboBoxOptionstray_dash_2")
    opt_tray3: Final = CSS("#ComboBoxOptionstray_dash_3")
    opt_tray4: Final = CSS("#ComboBoxOptionstray_dash_4")
    opt_tray5: Final = CSS("#ComboBoxOptionstray_dash_5")
    opt_tray6: Final = CSS("#ComboBoxOptionstray_dash_6")
    opt_tray_auto: Final = CSS("#ComboBoxOptionsauto_")
    opt_tray_alternate: Final = CSS("#ComboBoxOptionsalternate")
    opt_tray_manual: Final = CSS("#ComboBoxOptionsmanual")
    opt_tray_main: Final = CSS("#ComboBoxOptionsmain")

    # Dinámicos (ejemplo): opción de bandeja por nombre
    tray_option: Callable[[str], Locator] = staticmethod(lambda name: CSS(f"[data-test='tray-{name}']"))
    # Parametrizado por índice (ajusta formato a tu UDW si lo necesita)
    paper_tray_by_index: Callable[[int], Locator] = staticmethod(lambda n: OID(f"cTrayN:{n}"))

    # ------------------------------- Output scale / resize -------------------------- #
    list_output_scale: Final = CSS("#copySettingResize")
    view_output_scale: Final = CSS("#copyResizeView")
    btn_output_scale_back: Final = CSS("#copyResizeView #BackButton")
    value_output_scale: Final = CSS("#copySettingResize_2infoBlockRow")
    radio_output_scale_none: Final = CSS("#none")
    row_output_scale_none: Final = CSS("#noneRow")
    radio_output_scale_custom: Final = CSS("#customRadioButton")
    row_output_scale_custom: Final = CSS("#customRow")
    spinbox_output_scale_custom: Final = CSS("#custom")
    radio_output_scale_fit_to_page: Final = CSS("#fitToPage")
    row_output_scale_fit_to_page: Final = CSS("#fitToPageRow")
    radio_output_scale_full_page: Final = CSS("#fullPage")
    row_output_scale_full_page: Final = CSS("#fullPageRow")
    radio_output_scale_legal_to_letter: Final = CSS("#legalToLetter")
    row_output_scale_legal_to_letter: Final = CSS("#legalToLetterRow")
    radio_output_scale_letter_to_a4_94: Final = CSS("#letterToA4")
    row_output_scale_letter_to_a4_94: Final = CSS("#letterToA4Row")
    radio_output_scale_a4_to_letter_91: Final = CSS("#a4ToLetter")
    row_output_scale_a4_to_letter_91: Final = CSS("#a4ToLetterRow")
    check_output_scale_include_margins: Final = CSS("#fitToPageIncludeMargin")
    row_output_scale_include_margins: Final = CSS("#CheckBoxOptionsfitToPageIncludeMargin")

    # ------------------------------- Preview / pre-preview -------------------------- #
    button_preview: Final = CSS("#previewButton")
    button_preview_large: Final = CSS("#previewButtonLargeScreen")
    button_refresh_preview: Final = CSS("#refreshPanelButton")
    refresh_modal_dialog: Final = CSS("#refreshPreviewPanel")
    preview_image: Final = CSS("#image_0")
    refresh_modal_dialog_refresh: Final = CSS("#refreshPreviewButton")
    button_collapse_secondary_panel: Final = CSS("#_CollapseButton")
    button_expand_secondary_panel: Final = CSS("#_ExpandButton")
    preview_panel: Final = CSS("#itempreview")
    button_start_copy_main_panel: Final = CSS("#mainActionButtonOfMainPanel")
    cancel_button_preview_panel: Final = CSS("#cancelButtonPreviewPanel")
    pre_preview_layout: Final = CSS("#prePreview")
    pre_preview_content: Final = CSS("#contentText")
    pre_preview_animation: Final = CSS("#animationImage")
    copy_cancel_button: Final = CSS("#cancelButton")
    duplex_copy_continue: Final = CSS("#Continue")
    drop_down_button: Final = CSS("#dropDownButton")

    # ------------------------------- Toast / constraints ---------------------------- #
    view_system_toast: Final = CSS("#SpiceToast")
    constraint_view: Final = CSS("#ConstraintMessage")
    constraint_message_text: Final = CSS("#ConstraintMessage #constraintDescription SpiceText[objectName=contentItem]")
    constraint_ok_button: Final = CSS("#ConstraintMessage #okButton")

    # ------------------------------- Some dynamic helpers (ejemplo) ----------------- #
    # Ids parametrizados de papel/bandeja como 'object_id'
    media_size_option_by_sid: Callable[[str], Locator] = staticmethod(lambda sid: OID(sid))

    # ------------------------------- String IDs (como object_id) -------------------- #
    # (Usados por APIs que buscan por id semántico en lugar de CSS)
    # --- Media size IDs ---
    sid_media_size_custom: Final = OID("cMediaSizeIdCustom")
    sid_media_size_arch_a: Final = OID("cMediaSizeIdArchA")
    sid_media_size_arch_b: Final = OID("cMediaSizeIdArchB")
    sid_media_size_arch_c: Final = OID("cMediaSizeIdArchC")
    sid_media_size_arch_d: Final = OID("cMediaSizeIdArchD")
    sid_media_size_arch_e: Final = OID("cMediaSizeIdArchE")
    sid_media_size_arch_e2: Final = OID("cMediaSizeIdArchE2")
    sid_media_size_arch_e3: Final = OID("cMediaSizeIdArchE3")
    sid_media_size_a2: Final = OID("cMediaSizeIdA2")
    sid_media_size_a3: Final = OID("cMediaSizeIdA3")
    sid_media_size_a4: Final = OID("cMediaSizeIdA4")
    sid_media_size_a5: Final = OID("cMediaSizeIdA5")
    sid_media_size_a6: Final = OID("cMediaSizeIdA6")
    sid_media_size_a4_rot: Final = OID("cMediaSizeIdA4Rotated")
    sid_media_size_a5_rot: Final = OID("cMediaSizeIdA5Rotated")
    sid_media_size_iso_b0: Final = OID("cMediaSizeIdISOB0")
    sid_media_size_iso_b1: Final = OID("cMediaSizeIdISOB1")
    sid_media_size_iso_b2: Final = OID("cMediaSizeIdISOB2")
    sid_media_size_iso_b3: Final = OID("cMediaSizeIdISOB3")
    sid_media_size_iso_b4: Final = OID("cMediaSizeIdISOB4")
    sid_media_size_b5_rot: Final = OID("cMediaSizeIdJisB5Rotated")
    sid_media_size_envelope_b5: Final = OID("cMediaSizeIdB5Envelope")
    sid_media_size_jis_b6: Final = OID("cMediaSizeIdJisB6")
    sid_media_size_envelope_monarch: Final = OID("cMediaSizeIdMonarchEnvelope")
    sid_media_size_c0: Final = OID("cMediaSizeIdC0")
    sid_media_size_c1: Final = OID("cMediaSizeIdC1")
    sid_media_size_c2: Final = OID("cMediaSizeIdC2")
    sid_media_size_c3: Final = OID("cMediaSizeIdC3")
    sid_media_size_c4: Final = OID("cMediaSizeIdC4")
    sid_media_size_envelope_c5: Final = OID("cMediaSizeIdC5Envelope")
    sid_media_size_envelope_c6: Final = OID("cMediaSizeIdEnvelopeC6")
    sid_media_size_envelope_dl: Final = OID("cMediaSizeIdDLEnvelope")
    sid_media_size_j_chou3: Final = OID("cMediaSizeIdJChou3Envelope")
    sid_media_size_j_chou4: Final = OID("cMediaSizeIdJChou4Envelope")
    sid_media_size_hagaki: Final = OID("cMediaSizeIdHagaki")
    sid_media_size_double_postcard: Final = OID("cMediaSizeIdOfukuHagaki")
    sid_media_size_4x6: Final = OID("cMediaSizeIdFourXSix")
    sid_media_size_5x7: Final = OID("cMediaSizeIdFiveXSeven")
    sid_media_size_5x8: Final = OID("cMediaSizeIdFiveXEight")
    sid_media_size_letter: Final = OID("cMediaSizeIdLetter")
    sid_media_size_letter_rot: Final = OID("cMediaSizeIdLetterRotated")
    sid_media_size_legal: Final = OID("cMediaSizeIdLegal")
    sid_media_size_envelope_com10: Final = OID("cMediaSizeIdCOM10Envelope")
    sid_media_size_executive: Final = OID("cMediaSizeIdExecutive")
    sid_media_size_oficio: Final = OID("cMediaSizeIdOficio")
    sid_media_size_16k_184x260: Final = OID("cMediaSizeIdSize16K184x260")
    sid_media_size_16k_195x270: Final = OID("cMediaSizeIdSize16k195x270")
    sid_media_size_16k: Final = OID("cMediaSizeIdSixteenK")
    sid_media_size_b5: Final = OID("cMediaSizeIdJisB5")
    sid_media_size_statement: Final = OID("cMediaSizeIdStatement")
    sid_media_size_oficio_216x340: Final = OID("cMediaSizeIdOficio216x340")
    sid_media_size_ledger_11x17: Final = OID("cMediaSizeIdLedger")
    sid_media_size_100x150mm: Final = OID("cMediaSizeId10x15cm")
    sid_media_size_d_22x34in: Final = OID("cMediaSizeIdANSID")
    sid_media_size_e_34x44in: Final = OID("cMediaSizeIdANSIE")
    sid_media_size_2l_127x178: Final = OID("cMediaSizeIdSize2L")
    sid_media_size_env_6_75: Final = OID("cMediaSizeIdEnvelope6ThreeQuarter")
    sid_media_size_super_b: Final = OID("cMediaSizeIdSuperB")
    sid_media_size_arch_e1: Final = OID("cMediaSizeIdArchE1")
    sid_media_size_l_3_5x5in: Final = OID("cMediaSizeIdSizeL9x13cm")
    sid_media_size_env_9: Final = OID("cMediaSizeIdEnvelope9")
    sid_media_size_4x12in: Final = OID("cMediaSizeIdFourXTwelveTenXThirty")
    sid_media_size_4x5in: Final = OID("cMediaSizeIdFourXFiveTenXThirteen")
    sid_media_size_5x5in: Final = OID("cMediaSizeIdFiveXFiveThirteenXThirteen")
    sid_media_size_8k_260x368: Final = OID("cMediaSizeIdSize8K260x368")
    sid_media_size_8k_270x390: Final = OID("cMediaSizeIdSize8K270x390")
    sid_media_size_8k_273x394: Final = OID("cMediaSizeIdEightK")
    sid_media_size_ra3: Final = OID("cMediaSizeIdRA3")
    sid_media_size_ra4: Final = OID("cMediaSizeIdRA4")
    sid_media_size_sra3: Final = OID("cMediaSizeIdSra3")
    sid_media_size_sra4: Final = OID("cMediaSizeIdSra4")
    sid_media_size_jis_b0: Final = OID("cMediaSizeIdJISB0")
    sid_media_size_jis_b1: Final = OID("cMediaSizeIdJISB1")
    sid_media_size_jis_b2: Final = OID("cMediaSizeIdJISB2")
    sid_media_size_jis_b3: Final = OID("cMediaSizeIdJISB3")
    sid_media_size_jis_b4: Final = OID("cMediaSizeIdJisB4")
    sid_media_size_ansi_c: Final = OID("cMediaSizeIdANSIC")
    sid_media_size_11x14in: Final = OID("cMediaSizeIdElevenXFourteen")
    sid_media_size_8x10in: Final = OID("cMediaSizeIdEightXTen")
    sid_media_size_index_3x5: Final = OID("cMediaSizeIdThreeXFive")
    sid_media_size_any: Final = OID("cMediaSizeIdAny")
    sid_media_size_env_a2: Final = OID("cMediaSizeIdA2Envelope")
    sid_media_size_mixed_letter_legal: Final = OID("cMediaSizeIdMixedLetterLegal")
    sid_media_size_mixed_letter_ledger: Final = OID("cMediaSizeIdMixedLetterLedger")
    sid_media_size_mixed_a4_a3: Final = OID("cMediaSizeIdMixedA4A3")

    # --- Paper tray (ids con parámetro) ---
    sid_paper_tray_n: Callable[[int], Locator] = staticmethod(lambda n: OID(f"cTrayN:{n}"))
    sid_paper_tray_auto: Final = OID("cAutomatic")

    # --- Pages per sheet (ids) ---
    sid_pages_oneup: Final = OID("cOutputNupCountTypeONE")
    sid_pages_twoup: Final = OID("cTwo")
    sid_pages_four_right_then_down: Final = OID("cFourRightThenDown")
    sid_pages_four_down_then_right: Final = OID("cOutputNupCountTypeFour")

    # --- Content type (ids) ---
    sid_content_mixed: Final = OID("cMixed")
    sid_content_photo: Final = OID("cScanModeGlossy")
    sid_content_text: Final = OID("cScanModeText")
    sid_content_lines: Final = OID("cLines")
    sid_content_image: Final = OID("cImage")

    # --- Quality (ids) ---
    sid_quality_standard: Final = OID("cStandard")
    sid_quality_best: Final = OID("cBestLabel")
    sid_quality_draft: Final = OID("cDraft")

    # --- Copy/scan labels (ids) ---
    sid_copy: Final = OID("cCopy")
    sid_preview: Final = OID("cPreviewLabel")
    sid_done_button: Final = OID("cDoneButton")
    sid_start: Final = OID("cStart")

    # ------------------------------- Sides (string IDs) ----------------------------- #
    sid_sides_1to1: Final = OID("c1To1Sided")
    sid_sides_1to2: Final = OID("c1To2Sided")
    sid_sides_2to1: Final = OID("c2To1Sided")
    sid_sides_2to2: Final = OID("c2To2Sided")

    # ------------------------------- Output scale (string IDs) ---------------------- #
    sid_output_scale_none: Final = OID("cNone")
    sid_output_scale_fit_to_page: Final = OID("cFitToPage")
    sid_output_scale_full_page: Final = OID("cFullPage")
    sid_output_scale_legal_to_letter: Final = OID("cLegalToLetter")
    sid_output_scale_letter_to_a4: Final = OID("cLettertoA4")
    sid_output_scale_a4_to_letter: Final = OID("cA4ToLetter")
    sid_output_scale_custom: Final = OID("cCustomPara")

    # ------------------------------- Staple ---------------------------------------- #
    list_staple: Final = CSS("#copy_stapleSettingsTextImage")
    list_staple_value: Final = CSS("#copy_stapleSettingsTextImage_2infoBlockRow")
    list_staple_selection: Final = CSS("#copy_stapleMenuSelectionList")

    radio_staple_none: Final = CSS("#MenuValuenone")
    row_staple_none: Final = CSS("#nonecopy_staple")

    radio_staple_top_any_one_point_any: Final = CSS("#MenuValuetopAnyOnePointAny")
    row_staple_top_any_one_point_any: Final = CSS("#topAnyOnePointAnycopy_staple")

    radio_staple_top_left_one_point_any: Final = CSS("#MenuValuetopLeftOnePointAny")
    row_staple_top_left_one_point_any: Final = CSS("#topLeftOnePointAnycopy_staple")

    radio_staple_top_right_one_point_angled: Final = CSS("#MenuValuetopRightOnePointAngled")
    row_staple_top_right_one_point_angled: Final = CSS("#topRightOnePointAngledcopy_staple")

    radio_staple_left_two_points: Final = CSS("#MenuValueleftTwoPoints")
    row_staple_left_two_points: Final = CSS("#leftTwoPointscopy_staple")

    # Staple (string IDs)
    sid_staple_none: Final = OID("cNone")
    sid_staple_top_left_or_right: Final = OID("cStapleTopLeftOrRight")
    sid_staple_left_two_points: Final = OID("cStapleLeftTwoPoints")
    sid_staple_top_left_one_point_angled: Final = OID("cStapleTopLeftOnePointAngled")
    sid_staple_top_right_one_point_angled: Final = OID("cStapleTopRightOnePointAngled")

    # ------------------------------- Punch ----------------------------------------- #
    list_punch: Final = CSS("#copy_punchSettingsTextImage")
    list_punch_value: Final = CSS("#copy_punchSettingsTextImage_2infoBlockRow")
    list_punch_selection: Final = CSS("#copy_punchMenuSelectionList")

    radio_punch_none: Final = CSS("#MenuValuenone")
    row_punch_none: Final = CSS("#nonecopy_punch")

    radio_punch_left_two_point_din: Final = CSS("#MenuValueleftTwoPointDin")
    row_punch_left_two_point_din: Final = CSS("#leftTwoPointDincopy_punch")

    radio_punch_right_two_point_din: Final = CSS("#MenuValuerightTwoPointDin")
    row_punch_right_two_point_din: Final = CSS("#rightTwoPointDincopy_punch")

    # Punch (string IDs)
    sid_punch_none: Final = OID("cNone")
    sid_punch_left_two_points: Final = OID("cStapleLeftTwoPoints")
    sid_punch_right_two_points: Final = OID("cStapleRightTwoPoints")

    # ------------------------------- Fold ------------------------------------------ #
    list_fold: Final = CSS("#copySettingsfold")
    list_fold_value: Final = CSS("#copySettingsfold_2infoBlockRow")
    fold_selection_list: Final = CSS("#copyFoldView")

    radio_fold_vfold: Final = CSS("#V-fold")
    row_fold_vfold: Final = CSS("#V-foldRow")

    radio_fold_cfold: Final = CSS("#C-fold")
    row_fold_cfold: Final = CSS("#C-foldRow")

    row_fold_none: Final = CSS("#nonecopy_fold")

    # Fold (string IDs)
    sid_fold_none: Final = OID("cNone")
    sid_fold_c_inward_top: Final = OID("cInwardcFoldLeftUp")
    sid_fold_v_inward_top: Final = OID("cInwardVFold")

    # ------------------------------- Menú / carpetas Copy --------------------------- #
    view_menu_screen: Final = CSS("#landingPageMenuAppList")
    copy_folder_home_screen: Final = CSS("#copy")
    button_menu_copy: Final = CSS("#copyMenuApp")
    view_menu_copy_screen: Final = CSS("#copyMenuAppList")
    button_menu_copy_copy: Final = CSS("#cedab422-33b3-4638-b6a1-604e54525215MenuApp")
    scrollbar_menu_copy_folder: Final = CSS("#copyMenuAppListScrollBar")
    copy_folder_column_name: Final = CSS("#copyMenuAppListcolumn")
    copy_folder_content_item: Final = CSS("#copyMenuAppListlistItem")

    # ------------------------------- Copy Widget ----------------------------------- #
    widget_spinbox_copies: Final = CSS("#copyWidgetSpinBox")
    widget_button_start_copy: Final = CSS("#copyWidgetStartButton")
    widget_button_goto_copy_app: Final = CSS("#copyWidgetSettingsButton")
    widget_button_inc_copies: Final = CSS("#upBtn")
    widget_button_dec_copies: Final = CSS("#downBtn")
    button_save_as_default: Final = CSS("#savePanelButton")

    # ------------------------------- Quicksets / defaults --------------------------- #
    button_default_quickset: Final = CSS("#Default")
    quickset_mixed_content_id: Final = OID("61b72f38-1945-11ed-bf29-87d40f139a32")
    quickset_blueprint_id: Final = OID("eba1f540-239d-11ed-83d5-0b139473ea60")
    quickset_color_id: Final = OID("34cc69d4-194f-11ed-89dc-4be3ffadc2eb")
    quickset_greyscale_id: Final = OID("ccf3c448-250a-11ed-851e-d37653ac82ab")
    quickset_image_id: Final = OID("dba2ec94-250a-11ed-b62b-eb3183c3f17f")
    quickset_blueprint_red_stamp_id: Final = OID("c2306e7e-c4b7-11ed-a0a1-8776890b7239")

    view_menu_save_options: Final = CSS("#SaveOptionsForQSlist1")
    option_copy_as_defaults: Final = CSS("#AsDefaults")
    view_save_as_default_alert: Final = CSS("#ConfirmMessage")
    button_save_as_default_alert_save: Final = CSS("#messageSave")
    ok_under_save_option_view: Final = CSS("#saveoptionFooter #FooterViewRight #ContentItemText")

    defaults_and_quick_sets_view: Final = CSS("#SpiceListViewView")
    quickset_list_box: Final = CSS("#QSListofApp")
    quickset_selection_view: Final = CSS("#qsScroll")
    button_close_quicksets_view: Final = CSS("#CloseQuicksetList")
    qs_scroll_horizontal_bar: Final = CSS("#qsScrollhorizontalScroll")
    view_all_locator: Final = CSS("#ViewAll")
    ok_button_menu_quickset_no_quickset: Final = CSS("#OKButton")
    close_copy_settings_button: Final = CSS("#closeButton")

    text_toast_info: Final = CSS("#infoTextToastMessage")
    keyboard_view: Final = CSS("#spiceKeyboardView")
    ok_enter_key_positive_int: Final = CSS("#enterKeyPositiveIntegerKeypad")

    view_constraint_message: Final = CSS("#ConstraintMessage")
    constraint_message_text2: Final = CSS("#ConstraintMessage #constraintDescription SpiceText[objectName=contentItem]")
    ok_button_constraint_message: Final = CSS("#ConstraintMessage #okButton")

    # ------------------------------- Media mismatch --------------------------------- #
    media_mismatch_flow: Final = CSS("#mediaMismatchSizeFlowWindow")
    media_mismatch_alert_ok: Final = CSS("#OK")
    media_mismatch_alert_print: Final = CSS("#Print")
    media_mismatch_alert_hide: Final = CSS("#Hide")

    # ------------------------------- Output scale (detalle estándar) ---------------- #
    option_output_scale_menu: Final = CSS("#copySettingResize")
    output_scale_str_id: Final = OID("cOutputScale")
    option_output_scale_button: Final = CSS("#copySettingResize_2infoBlockRow")

    option_output_scale_loaded_paper: Final = CSS("#scaleToOutputRowRadioButton")
    option_output_scale_loaded_paper_detail: Final = CSS("#scaleToOutputRowComboBox")
    option_output_scale_loaded_paper_detail_roll: Final = CSS("#main_dash_roll")
    option_output_scale_loaded_paper_detail_tray: Final = CSS("#main")
    option_output_scale_loaded_paper_detail_roll_1: Final = CSS("#roll_dash_1")
    option_output_scale_loaded_paper_detail_sheet: Final = CSS("#top")

    option_output_scale_standard_sizes: Final = CSS("#standardSizeScalingRowRadioButton")
    option_output_scale_standard_sizes_detail: Final = CSS("#standardSizeScalingRowComboBox")
    opt_std_size_a0: Final = CSS("#iso_a0_841x1189mm")
    opt_std_size_a1: Final = CSS("#iso_a1_594x841mm")
    opt_std_size_a2: Final = CSS("#iso_a2_420x594mm")
    opt_std_size_a3: Final = CSS("#iso_a3_297x420mm")
    opt_std_size_a4: Final = CSS("#iso_a4_210x297mm")
    opt_std_size_b1: Final = CSS("#iso_b1_707x1000mm")
    opt_std_size_b2: Final = CSS("#iso_b2_500x707mm")
    opt_std_size_b3: Final = CSS("#iso_b3_353x500mm")
    opt_std_size_b4: Final = CSS("#iso_b4_250x353mm")
    opt_std_size_letter: Final = CSS("#na_letter_8_dot_5x11in")
    opt_std_size_ledger: Final = CSS("#na_ledger_11x17in")
    opt_std_size_ansi_c: Final = CSS("#na_c_17x22in")
    opt_std_size_ansi_d: Final = CSS("#na_d_22x34in")
    opt_std_size_ansi_e: Final = CSS("#na_e_34x44in")
    opt_std_size_arch_a: Final = CSS("#na_arch_dash_a_9x12in")
    opt_std_size_arch_b: Final = CSS("#na_arch_dash_b_12x18in")
    opt_std_size_arch_c: Final = CSS("#na_arch_dash_c_18x24in")
    opt_std_size_arch_d: Final = CSS("#na_arch_dash_d_24x36in")
    opt_std_size_arch_e: Final = CSS("#na_arch_dash_e_36x48in")
    standard_sizes_option_view: Final = CSS("#standardSizeScalingRowComboBoxpopupList")
    standard_sizes_scrollbar: Final = CSS("#comboBoxScrollBar")

    options_view_prefix: Final = CSS("#copySettingsPage_")
    options_view_scrollbar: Final = CSS("#copySettingsPage_list1ScrollBar")
    view_option_view: Final = CSS("#copySettingsPage_list1")

    copy_release_page_prompt_btn: Final = CSS("#CopyReleasePagebtn")
    copy_release_page_prompt: Final = CSS("#mdfEjectPage")

    spice_view: Final = CSS("#SpiceView")

    # ------------------------------- Active Job / Jobs app -------------------------- #
    copy_active_job_modal: Final = CSS("#ActiveJobModalView")
    copy_active_job_modal_text: Final = CSS("#ActiveJobModalView #textImage2 SpiceText[objectName=titleSmallItem]")
    copy_active_job_modal_header_text: Final = CSS("#ActiveJobModalView #SpiceHeaderVar1 SpiceText[objectName=titleObject]")
    copy_active_job_modal_ok: Final = CSS("#ActiveJobModalView #okButton")
    copy_adf_warning_modal_dialog: Final = CSS("#adfLoadedWarningModal")

    jobs_reprint_screen_cancel: Final = CSS("#cancelButtonJobReprintScreen")
    jobs_reprint_screen_spin_box: Final = CSS("#SpinCopiesJobReprintScreen")
    jobs_reprint_screen_reprint: Final = CSS("#reprintButtonJobReprintScreen")
    jobs_app_reprint_btn: Final = CSS("#reprintButton")
    jobs_app_delete_job_btn: Final = CSS("#deleteJobButton")
    jobs_app_delete_job_confirm_btn: Final = CSS("#deleteJobDeleteAnywayButton")

    copy_cancel_job_warning_prompt: Final = CSS("#CancelJobWarningPrompt")
    copy_cancel_job_warning_primary: Final = CSS("#CancelJobWarningPrompt #cancelJobWarningPrimaryButton")
    copy_cancel_job_warning_secondary: Final = CSS("#CancelJobWarningPrompt #cancelJobWarningSecondaryButton")

    copy_option_header_section: Final = CSS("#SpiceHeaderVar2")
    view_copy_widget_card_screen: Final = CSS("#widgetCardCopyApp")
    view_id_copy_screen: Final = CSS("#idCopyLandingView")
    button_id_copy_more_options: Final = CSS("#optionsDetailPanelButton")
    view_id_copy_settings: Final = CSS("#idCardCopySettingsPagelist1")
    app_copy_home_screen2: Final = CSS("#copy")

    collate_limit_warning_alert: Final = CSS("#collateProblemWindow")
    collate_limit_warning_ok: Final = CSS("#OK")

    more_pages_detected_collate_window: Final = CSS("#morePagesDetectedForCollateWindow")
    more_pages_collate_continue: Final = CSS("#CopyContinueButton")
    more_pages_collate_cancel: Final = CSS("#CopyCancelButton")

    button_add_page: Final = CSS("#previewFitPageContainer #scrollArea #grid #gridLayoutView  #gridLayout #addPageButton")
    button_ok_add_page: Final = CSS("#addPageOkButton")
    preview_add_page_prompt: Final = CSS("#previewAddPagePrompt")
    add_page_header: Final = CSS("#addpageHeader")
    pre_preview: Final = CSS("#prePreview")
    preview_warning_icon: Final = CSS("#icon_0")

    # ------------------------------- Stamps / Watermark ----------------------------- #
    sid_stamp_text_none: Final = OID("cNone")
    sid_stamp_text_draft: Final = OID("cDraft")
    sid_stamp_text_confidential: Final = OID("cConfidential")
    sid_stamp_text_secret: Final = OID("cSecret")
    sid_stamp_text_top_secret: Final = OID("cTopSecret")
    sid_stamp_text_urgent: Final = OID("cUrgent")

    row_combo_watermark_type: Final = CSS("#scan_watermarkTypeSettingsComboBox")
    combo_watermark_type: Final = CSS("#scan_watermarkTypeComboBox")
    view_watermark_type: Final = CSS("#scan_watermarkTypeComboBoxpopupList")
    opt_watermark_type_none: Final = CSS("#ComboBoxOptionsnone")
    opt_watermark_type_text: Final = CSS("#ComboBoxOptionstextWatermark")

    button_watermark_text_more_options: Final = CSS("#fromMoreOptions")
    view_watermark_text_more_options: Final = CSS("#scan_watermarkTextView")
    watermark_done_button: Final = CSS("#scan_watermarkMenuList #doneButton")
    copy_combobox_scrollbar: Final = CSS("#comboBoxScrollBar")
    scan_watermark_text_view_scrollbar: Final = CSS("#scan_watermarkTextViewScrollBar")
    scan_watermark_constraints_message: Final = OID("cUserWatermarkLimit")

    list_watermark: Final = CSS("#scanSettingswatermark")
    list_view_watermark: Final = CSS("#scan_watermarkMenuList")
    list_watermark_value: Final = CSS("#scanSettingswatermark_2infoBlockRow")
    copy_watermark_options_scrollbar: Final = CSS("#scan_watermarkMenuListScrollBar")

    list_watermark_text: Final = CSS("#scan_watermarkText")
    list_watermark_first_page_only: Final = CSS("#scan_firstPageOnly")
    list_watermark_text_font: Final = CSS("#scan_watermarkTextFontComboBox")
    list_watermark_text_size: Final = CSS("#scan_watermarkTextSizeComboBox")

    list_darkness: Final = CSS("#scan_watermarkDarknessMenuSlider")
    row_darkness: Final = CSS("#scan_watermarkDarknessSettingsSlider")

    radio_watermark_text_draft: Final = CSS("#draftRadioButton")
    row_watermark_text_draft: Final = CSS("#draftRadioButtonRow")
    radio_watermark_text_confidential: Final = CSS("#confidentialRadioButton")
    row_watermark_text_confidential: Final = CSS("#confidentialRadioButtonRow")
    radio_watermark_text_secret: Final = CSS("#secretRadioButton")
    row_watermark_text_secret: Final = CSS("#secretRadioButtonRow")
    radio_watermark_text_top_secret: Final = CSS("#topSecretRadioButton")
    row_watermark_text_top_secret: Final = CSS("#topSecretRadioButtonRow")
    radio_watermark_text_urgent: Final = CSS("#urgentRadioButton")
    row_watermark_text_urgent: Final = CSS("#urgentRadioButtonRow")

    checkbox_first_page_only: Final = CSS("#onlyFirstPageCheckbox")

    row_combo_text_font: Final = CSS("#scan_watermarkTextFontSettingsComboBox")
    combo_text_font: Final = CSS("#scan_watermarkTextFontComboBox")
    view_text_font: Final = CSS("#scan_watermarkTextFontComboBoxpopupList")
    combo_text_font_letter_gothic: Final = CSS("#ComboBoxOptionsletterGothic")
    combo_text_font_antique_olive: Final = CSS("#ComboBoxOptionsantiqueOlive")
    combo_text_font_century_schoolbook: Final = CSS("#ComboBoxOptionscenturySchoolbook")
    combo_text_font_garamond: Final = CSS("ComboBoxOptionsgaramond")  # (sin '#', tal cual en origen)

    row_combo_text_size: Final = CSS("#scan_watermarkTextSizeSettingsComboBox")
    combo_text_size: Final = CSS("#scan_watermarkTextSizeComboBox")
    view_text_size: Final = CSS("#scan_watermarkTextSizeComboBoxpopupList")
    combo_text_size_30pt: Final = CSS("#ComboBoxOptionsthirtyPoint")
    combo_text_size_40pt: Final = CSS("#ComboBoxOptionsfortyPoint")
    combo_text_size_60pt: Final = CSS("#ComboBoxOptionssixtyPoint")

    list_text_color: Final = CSS("#scanSettingsStampWatermarkTextcolor")
    list_text_color_value: Final = CSS("#scanSettingsStampWatermarkTextcolor_2infoBlockRow")
    list_view_text_color: Final = CSS("#scanSettingsStampWatermarkTextColorView")
    text_color_options_scrollbar: Final = CSS("#scanSettingsStampWatermarkTextColorViewScrollBar")
    radio_text_color_black: Final = CSS("#blackRadioButton")
    row_text_color_black: Final = CSS("#blackRadioButtonRow")
    radio_text_color_yellow: Final = CSS("#yellowRadioButton")
    row_text_color_yellow: Final = CSS("#yellowRadioButtonRow")
    radio_text_color_green: Final = CSS("#greenRadioButton")
    row_text_color_green: Final = CSS("#greenRadioButtonRow")
    radio_text_color_red: Final = CSS("#redRadioButton")
    row_text_color_red: Final = CSS("#redRadioButtonRow")
    radio_text_color_blue: Final = CSS("#blueRadioButton")
    row_text_color_blue: Final = CSS("#blueRadioButtonRow")
    radio_text_color_sky_blue: Final = CSS("#skyBlueRadioButton")
    row_text_color_sky_blue: Final = CSS("#skyBlueRadioButtonRow")
    radio_text_color_purple: Final = CSS("#purpleRadioButton")
    row_text_color_purple: Final = CSS("#purpleRadioButtonRow")

    watermark_text_field: Final = CSS("#scan_watermarkText")
    watermark_text_field_text: Final = CSS("#watermarkText")
    text_input: Final = CSS("#TextInput")
    button_keyboard_ok: Final = CSS("#enterKey1")

    slider_watermark_darkness: Final = CSS("#scan_watermarkDarknessMenuSlider")
    row_slider_watermark_darkness: Final = CSS("#scan_watermarkDarknessSettingsSlider")

    # String IDs (stamps/colors/fonts/sizes)
    #sid_stamp_text_none: Final = OID("cNone")
    sid_stamp_text_multiple: Final = OID("cMultiple")
    sid_stamp_required: Final = OID("cRequiredFieldLabel")
    sid_stamp_ip_address: Final = OID("cIPAddress")
    sid_stamp_user_name: Final = OID("cUserName")
    sid_stamp_product_info: Final = OID("cProductInformation")
    sid_stamp_page_number: Final = OID("cPageNumber")
    sid_stamp_date_time: Final = OID("cDateAndTime")
    sid_stamp_date: Final = OID("cDate")

    sid_stamp_number: Final = OID("cPageNumberingFormatTypePageFormat2")
    sid_stamp_page_plus_number: Final = OID("cPageNumberingFormatTypePageFormat1")
    sid_stamp_hyphen_number: Final = OID("cPageNumberingFormatTypePageFormat5")

    sid_stamp_font_antique: Final = OID("cAntiqueOlive")
    sid_stamp_font_century: Final = OID("cCenturySchoolbookFont")
    sid_stamp_font_garamond: Final = OID("cGaramond")
    sid_stamp_font_letter: Final = OID("cLetterGothic")

    sid_stamp_size_8pt: Final = OID("cStampTextSizeTypeSize8")
    sid_stamp_size_12pt: Final = OID("cStampTextSizeTypeSize12")
    sid_stamp_size_20pt: Final = OID("cStampTextSizeTypeSize20")

    sid_stamp_color_black: Final = OID("cColorBlack")
    sid_stamp_color_blue: Final = OID("cColorBlue")
    sid_stamp_color_green: Final = OID("cColorGreen")
    sid_stamp_color_purple: Final = OID("cColorPurple")
    sid_stamp_color_red: Final = OID("cColorRed")
    sid_stamp_color_sky_blue: Final = OID("cColorLightBlue")
    sid_stamp_color_yellow: Final = OID("cColorYellow")

    list_stamp_menu: Final = CSS("#scanSettingsStampsMenu")
    list_stamp_value: Final = CSS("#scanSettingsStampsMenu_2infoBlockRow")
    list_stamp_view: Final = CSS("#scan_stampsMenuList")
    stamp_location_view_back_button: Final = CSS("#scan_stampsMenuList #BackButton")
    stamp_view_scroll_bar: Final = CSS("#scan_stampsMenuListScrollBar")

    list_stamp_top_left: Final = CSS("#scan_stampTopLeftList")
    list_stamp_top_left_value: Final = CSS("#scan_stampTopLeftList_2infoBlockRow")

    list_stamp_top_center: Final = CSS("#scan_stampTopCenterList")
    list_stamp_top_center_value: Final = CSS("#scan_stampTopCenterList_2infoBlockRow")

    list_stamp_top_right: Final = CSS("#scan_stampTopRightList")
    list_stamp_top_right_value: Final = CSS("#scan_stampTopRightList_2infoBlockRow")

    list_stamp_bottom_left: Final = CSS("#scan_stampBottomLeftList")
    list_stamp_bottom_left_value: Final = CSS("#scan_stampBottomLeftList_2infoBlockRow")

    list_stamp_bottom_center: Final = CSS("#scan_stampBottomCenterList")
    list_stamp_bottom_center_value: Final = CSS("#scan_stampBottomCenterList_2infoBlockRow")

    list_stamp_bottom_right: Final = CSS("#scan_stampBottomRightList")
    list_stamp_bottom_right_value: Final = CSS("#scan_stampBottomRightList_2infoBlockRow")

    list_stamp_settings_view: Final = CSS("#stampSettingsView")
    stamp_settings_view_scroll_bar: Final = CSS("#stampSettingsViewScrollBar")

    stamp_settings_text_field: Final = CSS("#stampContentTextFeild #TextInput")
    stamp_settings_bubble: Final = CSS("#stampContentTextFeild #bubbleItem")
    stamp_settings_bubble1: Final = CSS("#stampContentTextFeild #bubbleItem0 #bubbleMouseArea")
    stamp_settings_bubble_text1: Final = CSS("#stampContentTextFeild #bubbleItem0 #EmailText")
    stamp_settings_content_button: Final = CSS("#stampContentButton")
    stamp_settings_done_button: Final = CSS("#stampSettingDoneButton")

    row_stamp_starting_page_spinbox: Final = CSS("#stampStartingPageSpinBoxRow")
    stamp_starting_page_spinbox: Final = CSS("#stampStartingPageSpinBox")
    stamp_starting_page_plus: Final = CSS("#stampStartingPageSpinBox #upBtn")
    stamp_starting_page_minus: Final = CSS("#stampStartingPageSpinBox #downBtn")
    stamp_starting_page_text: Final = CSS("#stampStartingPageSpinBox #SpinBoxTextInput")

    row_stamp_starting_number_spinbox: Final = CSS("#stampStartingNumberSpinBoxRow")
    stamp_starting_number_spinbox: Final = CSS("#stampStartingNumberSpinBox")
    stamp_starting_number_plus: Final = CSS("#stampStartingNumberSpinBox #upBtn")
    stamp_starting_number_minus: Final = CSS("#stampStartingNumberSpinBox #downBtn")
    stamp_starting_number_text: Final = CSS("#stampStartingNumberSpinBox #SpinBoxTextInput")

    row_stamp_number_of_digits_spinbox: Final = CSS("#stampNumberOfDigitsSpinBoxRow")
    stamp_number_of_digits_spinbox: Final = CSS("#stampNumberOfDigitsSpinBox")
    stamp_number_of_digits_plus: Final = CSS("#stampNumberOfDigitsSpinBox #upBtn")
    stamp_number_of_digits_minus: Final = CSS("#stampNumberOfDigitsSpinBox #downBtn")
    stamp_number_of_digits_text: Final = CSS("#stampNumberOfDigitsSpinBox #SpinBoxTextInput")

    stamp_combo_box_scrollbar: Final = CSS("#comboBoxScrollBar")
    view_stamp_combo_box: Final = CSS("#SettingsSpiceComboBoxpopupList")

    row_stamp_page_numbering_combo: Final = CSS("#stampPageNumberingComboBoxRow")
    stamp_page_numbering_combo: Final = CSS("#stampPageNumberingComboBoxRow #SettingsSpiceComboBox")
    combo_stamp_number: Final = CSS("#numberComboBox")
    combo_stamp_page_plus_number: Final = CSS("#pagePlusNumberComboBox")
    combo_stamp_hyphen_number: Final = CSS("#hyphenNumberHyphenComboBox")

    row_stamp_text_color: Final = CSS("#stampTextColorImageTextBranchRow")
    row_stamp_text_color_value: Final = CSS("#stampTextColorImageTextBranchRow_2infoBlockRow")

    row_stamp_text_font_combo: Final = CSS("#stampTextFontComboBoxRow")
    stamp_text_font_combo: Final = CSS("#stampTextFontComboBoxRow #SettingsSpiceComboBox")
    combo_stamp_antique_olive: Final = CSS("#antiqueOliveComboBox")
    combo_stamp_century_schoolbook: Final = CSS("#centurySchoolbookComboBox")
    combo_stamp_garamond: Final = CSS("#garamondComboBox")
    combo_stamp_letter_gothic: Final = CSS("#letterGothicComboBox")

    row_stamp_text_size_combo: Final = CSS("#stampTextSizeComboBoxRow")
    stamp_text_size_combo: Final = CSS("#stampTextSizeComboBoxRow #SettingsSpiceComboBox")
    combo_stamp_eight_point: Final = CSS("#eightPointComboBox")
    combo_stamp_twelve_point: Final = CSS("#twelvePointComboBox")
    combo_stamp_twenty_point: Final = CSS("#twentyPointComboBox")

    row_stamp_white_background_checkbox: Final = CSS("#stampWhiteBackgroundCheckBoxRow")
    stamp_white_background_checkbox: Final = CSS("#stampWhiteBackgroundCheckBox")

    list_stamp_content_view: Final = CSS("#stampContentView")
    stamp_content_done_button: Final = CSS("#stampContentDoneButton")
    stamp_content_edit_button: Final = CSS("#stampContentEditButton")
    stamp_content_view_scrollbar: Final = CSS("#stampContentViewScrollBar")

    row_stamp_ip_address_checkbox: Final = CSS("#ipAddressCheckBoxRow")
    stamp_ip_address_checkbox: Final = CSS("#ipAddressCheckBox")
    row_stamp_user_name_checkbox: Final = CSS("#userNameCheckBoxRow")
    stamp_user_name_checkbox: Final = CSS("#userNameCheckBox")
    row_stamp_product_info_checkbox: Final = CSS("#productInformationCheckBoxRow")
    stamp_product_info_checkbox: Final = CSS("#productInformationCheckBox")
    row_stamp_page_number_checkbox: Final = CSS("#pageNumberCheckBoxRow")
    stamp_page_number_checkbox: Final = CSS("#pageNumberCheckBox")
    row_stamp_date_time_checkbox: Final = CSS("#dateAndTimeCheckBoxRow")
    stamp_date_time_checkbox: Final = CSS("#dateAndTimeCheckBox")
    row_stamp_date_checkbox: Final = CSS("#dateCheckBoxRow")
    stamp_date_checkbox: Final = CSS("#dateCheckBox")
    row_stamp_user_defined_1_checkbox: Final = CSS("#userDefined1CheckBoxRow")
    stamp_user_defined_1_checkbox: Final = CSS("#userDefined1CheckBox")
    row_stamp_user_defined_2_checkbox: Final = CSS("#userDefined2CheckBoxRow")
    stamp_user_defined_2_checkbox: Final = CSS("#userDefined2CheckBox")
    row_stamp_user_defined_3_checkbox: Final = CSS("#userDefined3CheckBoxRow")
    stamp_user_defined_3_checkbox: Final = CSS("#userDefined3CheckBox")
    row_stamp_admin_defined_1_checkbox: Final = CSS("#adminDefined1CheckBoxRow")
    stamp_admin_defined_1_checkbox: Final = CSS("#adminDefined1CheckBox")
    row_stamp_admin_defined_2_checkbox: Final = CSS("#adminDefined2CheckBoxRow")
    stamp_admin_defined_2_checkbox: Final = CSS("#adminDefined2CheckBox")
    row_stamp_admin_defined_3_checkbox: Final = CSS("#adminDefined3CheckBoxRow")
    stamp_admin_defined_3_checkbox: Final = CSS("#adminDefined3CheckBox")

    list_stamp_edit_order_view: Final = CSS("#stampEditOrderView")
    stamp_edit_order_down_button: Final = CSS("#downButton")
    stamp_edit_order_up_button: Final = CSS("#upButton")
    stamp_edit_order_done_button: Final = CSS("#stampEditOrderDoneButton")
    stamp_edit_order_view_scrollbar: Final = CSS("#stampEditOrderViewScrollBar")

    row_stamp_ip_address_radio: Final = CSS("#ipAddressRadioButtonRow")
    stamp_ip_address_radio: Final = CSS("#ipAddressRadioButton")
    row_stamp_user_name_radio: Final = CSS("#userNameRadioButtonRow")
    stamp_user_name_radio: Final = CSS("#userNameRadioButton")
    row_stamp_product_info_radio: Final = CSS("#productInformationRadioButtonRow")
    stamp_product_info_radio: Final = CSS("#productInformationRadioButton")
    row_stamp_page_number_radio: Final = CSS("#pageNumberRadioButtonRow")
    stamp_page_number_radio: Final = CSS("#pageNumberRadioButton")
    row_stamp_date_time_radio: Final = CSS("#dateAndTimeRadioButtonRow")
    stamp_date_time_radio: Final = CSS("#dateAndTimeRadioButton")
    row_stamp_date_radio: Final = CSS("#dateRadioButtonRow")
    stamp_date_radio: Final = CSS("#dateRadioButton")
    row_stamp_user_defined_1_radio: Final = CSS("#userDefined1RadioButtonRow")
    stamp_user_defined_1_radio: Final = CSS("#userDefined1RadioButton")
    row_stamp_user_defined_2_radio: Final = CSS("#userDefined2RadioButtonRow")
    stamp_user_defined_2_radio: Final = CSS("#userDefined2RadioButton")
    row_stamp_admin_defined_1_radio: Final = CSS("#adminDefined1RadioButtonRow")
    stamp_admin_defined_1_radio: Final = CSS("#adminDefined1RadioButton")
    row_stamp_admin_defined_2_radio: Final = CSS("#adminDefined2RadioButtonRow")
    stamp_admin_defined_2_radio: Final = CSS("#adminDefined2RadioButton")

    # ------------------------------- Copy Mode / Modal ------------------------------ #
    copymode_button: Final = CSS("#copyModeMainPanelButton")
    copymode_modal_indirect_copy_radio: Final = CSS("#copyJobMode_afterScanningMenuRadioButton")
    copymode_modal_direct_copy_radio: Final = CSS("#copyJobMode_whileScanningMenuRadioButton")
    copymode_modal_interrupt_copy_toggle: Final = CSS("#copyJobMode_interruptToggleMenuSwitch")
    copymode_modal_close_button: Final = CSS("#closeButton")

    # ------------------------------- Load paper / ADF prompts ----------------------- #
    copy_load_paper_alert: Final = CSS("#mediaLoadFlowWindow")
    copy_adf_load_paper_alert: Final = CSS("#titleObject")
    adf_add_prompt_start_button: Final = CSS("#adfAddPageWindow #bodyLayoutverticalLayout #FooterView #startButton")
    adf_add_prompt_cancel_button: Final = CSS("#adfAddPageWindow #bodyLayoutverticalLayout #FooterView #CancelButton")
    copy_load_paper_ok: Final = CSS("#OK")
    copy_load_paper_hide: Final = CSS("#hide")

    # ------------------------------- Preview header -------------------------------- #
    copy_preview_header: Final = CSS("#previewHeader")
    copy_preview_header_more_options: Final = CSS("#moreOptions")
    copy_preview_edit_header: Final = CSS("#PreviewEditHeader")

    copy_preview_fitpage_container: Final = CSS("#previewFitPageContainer")
    copy_switch_preview_layout_button: Final = CSS("#switchPreviewLayoutButton")
    copy_preview_gridview_container: Final = CSS("#previewGridViewContainer")

    quick_copy_footer_spinbox: Final = CSS("#quickCopySpinBox")
    home_screen_footer: Final = CSS("#HomeScreenFooter")
    quick_copy_footer: Final = CSS("#copyQuickFooter")
    home_screen_footer_copy_button: Final = CSS("#QuickCopyButton")

    # ------------------------------- Book mode / Scan aids -------------------------- #
    scan_both_sides_for_book_mode: Final = CSS("#bookModeBothSidesRBModel")
    scan_skip_left_side_for_book_mode: Final = CSS("#bookModeSkipLeftSideRBModel")
    scan_skip_right_side_for_book_mode: Final = CSS("#bookModeSkipRightSideRBModel")
    button_scan_book_mode_instructions_scan: Final = CSS("#scanButton")
    book_mode_instructions_view: Final = CSS("#bookModeInstructionsView")
    button_scan_book_mode_instructions_finish: Final = CSS("#finishButton")
    scan_mode_done_button: Final = CSS("#copy_scanModeList #footerDoneButton")
    button_scan_book_mode_instructions_cancel: Final = CSS("#bookModeCancelButton")
    button_scan_add_page_flatbed_duplex_cancel_yes: Final = CSS("#yesButton")

    button_menu_preview_settings: Final = CSS("#imagePreviewSettingsSettingsTextImage")
    view_preview_screen: Final = CSS("#imagePreviewSettingsMenuList")
    view_copy_preview_configuration: Final = CSS("#copyPreviewSettingsTextImage_2infoBlockRow")

    scan_mode_back_button: Final = CSS("#copy_scanModeList #BackButton")
    copy_2_sided_id_prompt: Final = CSS("#scanManualDuplexSecondSide")
    copy_2_sided_id_scan_button: Final = CSS("#ScanButton")
    copy_2_sided_id_done_button: Final = CSS("#DoneButton")
    copy_2_sided_id_cancel_button: Final = CSS("#scanManualDuplexSecondSide #cancelButton")
    copy_2_sided_id_prompt_text: Final = CSS("#scanManualDuplexSecondSide #alertDetailDescription SpiceText[objectName=contentItem]")
    copy_flatbed_cancel_job_prompt_yes: Final = CSS("#FlatbedCancelPrompt #yesButton")

    spinbox_copy_mouse_area: Final = CSS("#CopyQuickWidget #SpinBoxTextFieldMouseArea")
    spinbox_ok_key: Final = CSS("#keyboard #enterKeyPositiveIntegerKeypad")
    select_best_quality: Final = CSS("#ComboBoxOptionsbest #ComboBoxOptionsbestRadioButtonModel")

    # ------------------------------- Cancel job (beam/active) ----------------------- #
    button_cancel_job: Final = CSS("#JobModalView #cancelButton")
    button_active_job_cancel: Final = CSS("#ActiveJobModalView #cancelJobButton")

    # ------------------------------- Alert App -------------------------------------- #
    alert_app_landing_view: Final = CSS("#alertAppView #alertAppHeader")
    alert_app_landing_view_close_button: Final = CSS("#alertAppView #alertAppHeader #closeButton")

    # ------------------------------- Output destination ----------------------------- #
    row_output_destination_combo: Final = CSS("#copy_outputDestinationSettingsComboBox")
    output_destination_combo: Final = CSS("#copy_outputDestinationComboBox")

    # ------------------------------- Misc ------------------------------------------- #
    stop_scan_button: Final = CSS("#stopScanButtonDetailRightBlock")
    no_access_view: Final = CSS("#noAccessView")
    no_access_ok_button: Final = CSS("#noAccessOkButton")
