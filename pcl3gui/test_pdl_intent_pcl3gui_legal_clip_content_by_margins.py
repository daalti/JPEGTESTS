import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a legal clip content by margins sheet PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-151979
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:legal_clip_content_by_margins.prn=7babfe7eb9221264705bc70afb1217542ea62b41a229e624462d7be8b7db01f2
    +name:test_pdl_intent_pcl3gui_legal_clip_content_by_margins
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_legal_clip_content_by_margins
        +guid:bf04ed54-42a5-4be0-8ed8-4d935f4d5cdc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & MediaSizeSupported=custom & Print=Normal & MediaType=Plain & MediaInputInstalled=MainRoll

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_legal_clip_content_by_margins(setup_teardown, printjob, outputsaver, tray, outputverifier):

    printjob.print_verify('7babfe7eb9221264705bc70afb1217542ea62b41a229e624462d7be8b7db01f2')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 2)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 3)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.blackandwhite)
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
