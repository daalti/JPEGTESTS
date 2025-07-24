import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, MediaType, MediaSource, Plex, PlexBinding


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print a PCL5 test file with media source command specified with tray2, plex command specified with duplex short edge and ensure PDL is processing the job with tray2 and producing duplex short edge output
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-183335, DUNE-187154
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:pcl5_duplex_shortedge_tray2.prn=4011e2a4035841c2b451ce07faf2dfda45e9311513a80ea036c5b440705ebb65
    +test_classification:Systems
    +name: test_pdl_intent_pcl5_duplex_shortedge_mediasource_tray2_2page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pdl_intent_pcl5_duplex_shortedge_mediasource_tray2_2page
        +guid:8ef3d98c-8621-4c92-8d70-8278c292768b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & MediaInputInstalled=Tray2 & MediaSizeSupported=na_letter_8.5x11in & Duplexer=True

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_intent_pcl5_duplex_shortedge_mediasource_tray2_2page(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_tray_supported('tray-2') and tray.is_size_supported('na_letter_8.5x11in', 'tray-2'):
        tray.configure_tray('tray-2', 'na_letter_8.5x11in', 'stationery')
        printjob.print_verify('4011e2a4035841c2b451ce07faf2dfda45e9311513a80ea036c5b440705ebb65')
        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 2)
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
        outputverifier.verify_collated_copies(Intents.printintent, 1)
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
        outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        outputverifier.verify_media_source(Intents.printintent, MediaSource.tray2)
        outputsaver.save_output()
        outputsaver.operation_mode('NONE')
        tray.reset_trays()
