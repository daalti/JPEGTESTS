import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a4 glossy 12-page duplex booklet on 2pages per sheet  PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-150020
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:a4_booklet_on_2pagespersheet.prn=aca719580d13eee0b00fc06c86cb0320262e89dded709a30431a71d4d19ee329
    +name:test_pdl_intent_pcl3gui_a4_bookleton_2pagespersheet
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_a4_bookleton_2pagespersheet
        +guid:0c48f1a7-5d0a-4bdd-9d2d-42d469f3e1bd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & PrintColorMode=GrayScale & Print=Normal & MediaType=HPTri-foldBrochurepaper-Glossy & MediaInputInstalled=Main & PrintResolution=Print600 & Duplexer=True

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_a4_bookleton_2pagespersheet(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('iso_a4_210x297mm', 'tray-1'):
        tray.configure_tray('tray-1', 'iso_a4_210x297mm', 'com.hp-trifold-brochure-glossy-180gsm')

    printjob.print_verify('aca719580d13eee0b00fc06c86cb0320262e89dded709a30431a71d4d19ee329')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent,12)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.grayscale)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.trifold_brochure_glossy)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
