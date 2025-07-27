import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a 4X6 plain 17-page simplex borderlessoff 6pages per sheet PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-150020
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:4X6_borderlessoff_6pagespersheet.prn=a25778f5e599f711872d388115a9e1f31a52c476ee3c0405a2f2387f261c7545
    +name:test_pdl_intent_pcl3gui_4X6_borderlessoff_6pagespersheet
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_4X6_borderlessoff_6pagespersheet
        +guid:f2ff6d79-4b89-46cb-8e16-cdf5d4d83454
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & PrintColorMode=BlackOnly & Print=Draft & MediaType=Plain & PrintResolution=Print300

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_4X6_borderlessoff_6pagespersheet(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('na_index-4x6_4x6in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_index-4x6_4x6in', 'stationery')

    printjob.print_verify('a25778f5e599f711872d388115a9e1f31a52c476ee3c0405a2f2387f261c7545')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 3)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.photo4x6)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.draft)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    outputverifier.verify_resolution(Intents.printintent, 300)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
