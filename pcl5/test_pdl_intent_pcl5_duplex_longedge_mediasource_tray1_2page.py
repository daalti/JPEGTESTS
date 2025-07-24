import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, MediaType, MediaSource, Plex, PlexBinding


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print a PCL5 test file with media source command specified with tray1, plex command specified with duplex long edge and ensure PDL is processing the job with tray1 and producing duplex long edge output
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-183335, DUNE-187154
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:pcl5_duplex_longedge_tray1.prn=d375b13a581607e4562b116af4585f5523757f255463204a43a6ce654e2080c0
    +test_classification:System
    +name: test_pdl_intent_pcl5_duplex_longedge_mediasource_tray1_2page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pdl_intent_pcl5_duplex_longedge_mediasource_tray1_2page
        +guid:3dc4d7d5-98fd-49f5-94e0-5c2a50b59f77
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & MediaInputInstalled=Tray1 & MediaSizeSupported=na_letter_8.5x11in & Duplexer=True

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_intent_pcl5_duplex_longedge_mediasource_tray1_2page(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_tray_supported('tray-1') and tray.is_size_supported('na_letter_8.5x11in', 'tray-1'):
        tray.configure_tray('tray-1', 'na_letter_8.5x11in', 'stationery')
        printjob.print_verify('d375b13a581607e4562b116af4585f5523757f255463204a43a6ce654e2080c0')
        outputverifier.save_and_parse_output()
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
        outputverifier.verify_page_count(Intents.printintent, 2)
        outputverifier.verify_collated_copies(Intents.printintent, 1)
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
        outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
        outputsaver.save_output()
        outputsaver.operation_mode('NONE')
        tray.reset_trays()
