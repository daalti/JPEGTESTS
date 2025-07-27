import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a Envelope#10 simplex borderless off 2pagesper sheet PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-150020
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Envelope10_borderless_off_2pagespersheet.prn=eab79f35370411ba7dc3bf1844bcc2db57e0f4a1cd0ce3602b373591cd41be04
    +name:test_pdl_intent_pcl3gui_Envelope10_borderless_off_2pagespersheet
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_Envelope10_borderless_off_2pagespersheet
        +guid:f83696ad-9185-48fa-8880-9a3378c59b75
        +dut:
            +type:Simulator
            # +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=na_number-10_4.125x9.5in & PrintColorMode=Color & Print=Normal & MediaType=Plain & MediaInputInstalled=Main & PrintResolution=Print600

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_Envelope10_borderless_off_2pagespersheet(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_tray_supported('main'):
        if tray.is_size_supported('na_number-10_4.125x9.5in', 'main'):
            tray.configure_tray('main', 'na_number-10_4.125x9.5in', 'stationery')
            printjob.print_verify('eab79f35370411ba7dc3bf1844bcc2db57e0f4a1cd0ce3602b373591cd41be04')
            outputverifier.save_and_parse_output()
            outputverifier.verify_page_count(Intents.printintent, 3)
            outputverifier.verify_collated_copies(Intents.printintent, 1)
            outputverifier.verify_uncollated_copies(Intents.printintent, 1)
            outputverifier.verify_media_size(Intents.printintent, MediaSize.com10envelope)
            outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
            outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
            outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
            outputverifier.verify_plex(Intents.printintent, Plex.simplex)
            outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
            outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
            outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
            outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
            outputverifier.verify_resolution(Intents.printintent, 600)
            outputsaver.save_output()
            outputsaver.operation_mode('NONE')
            tray.reset_trays()
