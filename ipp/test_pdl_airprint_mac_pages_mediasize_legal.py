import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, ColorMode, PrintQuality, Plex, PlexBinding, MediaType, ContentOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pages document from mac and using attribute value media size legal
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-124180
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:legal_us_v5.bin=6cec019c068346ae4b8b6fdd3d7a4e0ba9c9b8e0a9764c60c6baa62e83448c41
    +test_classification:System
    +name:test_pdl_airprint_mac_pages_mediasize_legal
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_airprint_mac_pages_mediasize_legal
        +guid:7d1f90c1-fb7a-4330-8b9f-321462de6215
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_legal_8.5x14in & Print=Normal & Duplexer=True & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_airprint_mac_pages_mediasize_legal(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')
    default = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_legal_8.5x14in', 'print-color-mode': 'color', 'print-quality': 4, 'orientation-requested': 3, 'media-source': 'tray-1', 'media-type': 'auto', 'sides': 'one-sided'}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_legal_8.5x14in', 'print-color-mode': 'monochrome', 'print-quality': 4, 'orientation-requested': 3, 'media-source': 'tray-1', 'media-type': 'auto', 'sides': 'one-sided'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6cec019c068346ae4b8b6fdd3d7a4e0ba9c9b8e0a9764c60c6baa62e83448c41')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 3)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.legal)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()