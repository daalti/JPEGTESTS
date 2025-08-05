import pytest
from dunetuf.print.output.intents import Intents, MediaSize, Plex, PlexBinding, ColorMode, MediaSource
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value sides_two-sided-short-edge.
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
    +name:test_pdl_intent_ipp_jpg_sides_two_sided_short_edge
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_jpg_sides_two_sided_short_edge
        +guid:665dde4b-70bf-4ce9-baba-3c4981f664dd
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & Duplexer=True & MediaSizeSupported=na_letter_8.5x11in & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_jpg_sides_two_sided_short_edge(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):
    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'image/jpeg', 'sides': 'two-sided-short-edge', 'media-size-name' : 'na_letter_8.5x11in', 'print-color-mode': 'color', 'copies':1, 'media-source': 'tray-1'}
    else:
        ipp_test_attribs = {'document-format': 'image/jpeg', 'sides': 'two-sided-short-edge', 'media-size-name' : 'na_letter_8.5x11in', 'print-color-mode': 'monochrome', 'copies':1, 'media-source': 'tray-1'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    # single page duplex job requests should be considered as simplex
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    tray.reset_trays()