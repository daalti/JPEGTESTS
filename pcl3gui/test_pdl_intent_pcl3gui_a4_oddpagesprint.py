import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a4 glossy 12-page with print only odd pages PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-150020
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:a4_oddpagesprint.prn=0744f4ca1abcc420491d7973ef4e071f407a4f1347ea6619aca400b887557250
    +name:test_pdl_intent_pcl3gui_a4_oddpagesprint
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_a4_oddpagesprint
        +guid:b6cba5ea-0f1a-49dc-8880-963295bc61a4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & PrintColorMode=Color & Print=Normal & MediaInputInstalled=Main & PrintResolution=Print600 & BorderLessPrinting=True

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_a4_oddpagesprint(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('iso_a4_210x297mm', 'tray-1'):
        tray.configure_tray('tray-1', 'iso_a4_210x297mm', 'com.hp-matte-presentation')
        printjob.print_verify('0744f4ca1abcc420491d7973ef4e071f407a4f1347ea6619aca400b887557250')
        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent,6)
        outputverifier.verify_collated_copies(Intents.printintent, 1)
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
        outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
        outputverifier.verify_resolution(Intents.printintent, 600)
        outputsaver.save_output()
        outputsaver.operation_mode('NONE')
        tray.reset_trays()
