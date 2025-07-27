import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a ofuku hagaki plain 12-page simplex borderlessoff 9pages per sheet  PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-150020
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:ofuku_hagaki_borderlessoff_9pagespersheet.prn=795a889f75bdcf6de735ef426e8fcd9db3ab45c5b4402d70e6ce34c74eca18ba
    +name:test_pdl_intent_pcl3gui_ofuku_hagaki_borderlessoff_9pagespersheet
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_ofuku_hagaki_borderlessoff_9pagespersheet
        +guid:3571732e-66a9-4854-b7ff-b5c19439855f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=jpn_oufuku_148x200mm & PrintColorMode=BlackOnly & Print=Draft & MediaType=Plain & PrintResolution=Print300

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_ofuku_hagaki_borderlessoff_9pagespersheet(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('custom', 'tray-1'):
        tray.configure_tray('tray-1', 'custom', 'stationery')

    printjob.print_verify('795a889f75bdcf6de735ef426e8fcd9db3ab45c5b4402d70e6ce34c74eca18ba')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 2)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.draft)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    outputverifier.verify_resolution(Intents.printintent, 300)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
