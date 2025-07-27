import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a US Letter plain 13-page duplex borderlessoff 4pages per sheet  PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-150020
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter_borderlessoff_longedge_4pagespersheet.prn=79561232b571af0d7b61a2f099979bd16c45fe768bc252edd4f8d8927b33a1e1
    +name:test_pdl_intent_pcl3gui_letter_borderlessoff_4pagespersheet
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_letter_borderlessoff_4pagespersheet
        +guid:c58984a4-4578-48f3-aaa0-2502abf401a4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & PrintColorMode=BlackOnly & Print=Best & MediaType=Plain  & PrintResolution=Print600 & Duplexer=True
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_letter_borderlessoff_4pagespersheet(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('na_letter_8.5x11in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('79561232b571af0d7b61a2f099979bd16c45fe768bc252edd4f8d8927b33a1e1')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 4)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.best)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
