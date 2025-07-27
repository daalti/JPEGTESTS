import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a letter simplex 2 copies PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-151979
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter_2copies.prn=b6262016518cbb0e85e82263bc46c82f6c381e8b5453397226ada1e68206ca4d
    +name:test_pdl_intent_pcl3gui_letter_2copies
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_letter_2copies
        +guid:6863e934-64de-447b-a262-061ee16a4d15
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & MediaSizeSupported=na_letter_8.5x11in & PrintColorMode=Color & Print=Normal & MediaType=Plain & MediaInputInstalled=Main

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_letter_2copies(setup_teardown, printjob, outputsaver, tray, outputverifier):

    printjob.print_verify('b6262016518cbb0e85e82263bc46c82f6c381e8b5453397226ada1e68206ca4d')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 3)
    outputverifier.verify_collated_copies(Intents.printintent, 2)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()