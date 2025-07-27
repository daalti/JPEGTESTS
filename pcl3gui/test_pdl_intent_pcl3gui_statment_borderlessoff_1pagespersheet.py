import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a statement plain 6-page simplex borderlessoff 1page per sheet  PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-150020
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:statment_borderlessoff_1pagespersheet.prn=4f770b832c8c8b44076c3c3eaacf57ff29b4b2198420020ab1d8a5bd2a01c3b4
    +name:test_pdl_intent_pcl3gui_statment_borderlessoff_1pagespersheet
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_statment_borderlessoff_1pagespersheet
        +guid:abaa98cb-0106-4f76-bd72-8fa582183792
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=na_invoice_5.5x8.5in & PrintColorMode=GrayScale & Print=Normal & MediaType=Plain & PrintResolution=Print600

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_statment_borderlessoff_1pagespersheet(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('na_invoice_5.5x8.5in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_invoice_5.5x8.5in', 'stationery')

    printjob.print_verify('4f770b832c8c8b44076c3c3eaacf57ff29b4b2198420020ab1d8a5bd2a01c3b4')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 6)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.statement)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.grayscale)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_plex(Intents.printintent, Plex.simplex)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
