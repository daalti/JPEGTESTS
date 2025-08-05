import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, ColorMode, PrintQuality, Plex, PlexBinding, MediaType, ContentOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pages document from mac and using attribute value mediasize Letter
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-124180
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter_us_v5.bin=9464f40b9055c57e8f5f0abed54a2e7896e7dd0bc30ed423d469345efb6a1300
    +test_classification:System
    +name:test_pdl_airprint_mac_pages_mediasize_Letter
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_airprint_mac_pages_mediasize_Letter
        +guid:28705115-b98d-42dc-9d03-5827b020bda3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & Print=Normal & Duplexer=True & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_airprint_mac_pages_mediasize_Letter(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_letter_8.5x11in', 'print-color-mode': 'color', 'print-quality': 4, 'sides': 'two-sided-short-edge', 'media-type': 'auto', 'orientation-requested': 4, 'media-source': 'tray-1'}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_letter_8.5x11in', 'print-color-mode': 'monochrome', 'print-quality': 4, 'sides': 'two-sided-short-edge', 'media-type': 'auto', 'orientation-requested': 4, 'media-source': 'tray-1'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '9464f40b9055c57e8f5f0abed54a2e7896e7dd0bc30ed423d469345efb6a1300')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 4)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()