import pytest
import logging
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, PrintQuality, ColorMode, ContentOrientation, ColorRenderingType, Plex, PlexBinding, PlexSide, MediaType, MediaSize

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value print-quality_high.
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
    +name:test_pdl_intent_ipp_jpg_print_quality_high
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_jpg_print_quality_high
        +guid:8f350506-f6b3-4763-82a9-95bd617f8dcf
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & Print=Best
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_jpg_print_quality_high(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm, configuration):
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'image/jpeg', 'print-quality': print_quality_high, 'print-color-mode': 'color', 'orientation-requested': 3, 'sides': 'one-sided', 'media-type': 'stationery', 'copies':5, 'media': 'na_letter_8.5x11in'}
    else:
        ipp_test_attribs = {'document-format': 'image/jpeg', 'print-quality': print_quality_high, 'print-color-mode': 'monochrome', 'orientation-requested': 3, 'sides': 'one-sided', 'media-type': 'stationery', 'copies':5, 'media': 'na_letter_8.5x11in'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()
    if tray.is_size_supported('custom', default) and tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"] >= 94500:
        # the size of print file should in max/min custom size of printer supported, then could set custom size
        tray.configure_tray(default, "custom", 'stationery')

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    outputverifier.save_and_parse_output()

    expected_media_size = MediaSize.custom if 'roll' in default else MediaSize.letter
    if configuration.productname != "victoriaplus":
        outputverifier.verify_page_count(Intents.printintent, 1)
        outputverifier.verify_uncollated_copies(Intents.printintent, 5)
    else:
        outputverifier.verify_page_count(Intents.printintent, 5)
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[print_quality_high]])
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
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
        outputverifier.verify_plex_side(Intents.printintent, PlexSide.first)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    tray.reset_trays()