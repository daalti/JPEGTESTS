import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, ColorMode, PrintQuality, Plex, PlexBinding, MediaType, ContentOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a document from mac and using attribute value media type plain and media size Letter
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-124180
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:jpeg_vnd_landscape_normal.bin=1532e7f7a755ae9e38c5d7088b8cac96b266f21b73a8e2393c2acb3f372b7dd1
    +test_classification:System
    +name:test_pdl_airprint_mac_mediasize_letter_plain
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_airprint_mac_mediasize_letter_plain
        +guid:805186f5-635c-402c-b653-49229e37cfc1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & Print=Normal & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_airprint_mac_mediasize_letter_plain(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_letter_8.5x11in', 'print-color-mode': 'color', 'print-quality': 4, 'sides': 'one-sided', 'multiple-document-handling': 'separate-documents-collated-copies', 'orientation-requested': 4, 'media-type': 'stationery', 'media-source': 'tray-1'}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'na_letter_8.5x11in', 'print-color-mode': 'monochrome', 'print-quality': 4, 'sides': 'one-sided', 'multiple-document-handling': 'separate-documents-collated-copies', 'orientation-requested': 4, 'media-type': 'stationery', 'media-source': 'tray-1'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '1532e7f7a755ae9e38c5d7088b8cac96b266f21b73a8e2393c2acb3f372b7dd1')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()