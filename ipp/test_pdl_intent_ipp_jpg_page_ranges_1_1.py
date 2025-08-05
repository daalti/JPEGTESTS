import pytest
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value page_ranges_1_1
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_pdl_intent_ipp_jpg_page_ranges_1_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_jpg_page_ranges_1_1
        +guid:f56cfcee-853b-4cb4-9a08-1103587e1893
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_jpg_page_ranges_1_1(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm, configuration):
    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'image/jpeg', 'page-ranges': '1-1', 'copies':2, 'media': 'na_letter_8.5x11in', 'print-color-mode': 'color', 'orientation-requested': 3, 'sides': 'one-sided', 'media-type': 'stationery'}
    else:
        ipp_test_attribs = {'document-format': 'image/jpeg', 'page-ranges': '1-1', 'copies':2, 'media': 'na_letter_8.5x11in', 'print-color-mode': 'monochrome', 'orientation-requested': 3, 'sides': 'one-sided', 'media-type': 'stationery'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()
    if tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"] >= 150000:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, "custom", 'stationery')

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    outputverifier.save_and_parse_output()

    expected_media_size = MediaSize.custom if 'roll' in default else MediaSize.letter
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    if configuration.productname != "victoriaplus":
        outputverifier.verify_uncollated_copies(Intents.printintent, 2)
    else:
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    if configuration.familyname != "designjet":
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        if cdm.device_feature_cdm.is_color_supported():
            outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
        else:
            outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    tray.reset_trays()