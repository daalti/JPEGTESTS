import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a letter 1page clip content by margins sheet PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-151979
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter_clip_content_by_margin.prn=36dc77a06ebce648bc1b076192654ec233a98bdebfddb28dbd4a08c6ce19cc29
    +name:test_pdl_intent_pcl3gui_letter_clip_content_by_margin
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_letter_clip_content_by_margin
        +guid:55015d52-51ec-4eea-83eb-64394b413076
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & MediaSizeSupported=custom & PrintColorMode=Color & Print=Normal & MediaType=Plain & MediaInputInstalled=MainRoll

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_letter_clip_content_by_margin(setup_teardown, printjob, outputsaver, tray, outputverifier):

    printjob.print_verify('36dc77a06ebce648bc1b076192654ec233a98bdebfddb28dbd4a08c6ce19cc29')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 2)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.mainroll)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
