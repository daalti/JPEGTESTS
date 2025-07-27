import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a US Letter midweightglossy 12-page duplex borderless on PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-150020
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter_borderless_on.prn=f6f670fe00e1f836a29e968097da6e990e5b4eedf4b8036e280eac14386b33d1
    +name:test_pdl_intent_pcl3gui_letter_borderless_on
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_letter_borderless_on
        +guid:2f59a031-c830-4ff1-bbdb-cc7d8a1e2dc9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & PrintColorMode=GrayScale & Print=Normal & PrintResolution=Print600 & Duplexer=True

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_letter_borderless_on(setup_teardown, printjob, outputsaver, tray, outputverifier):


    printjob.print_verify('f6f670fe00e1f836a29e968097da6e990e5b4eedf4b8036e280eac14386b33d1')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 12)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.grayscale)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
