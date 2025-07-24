import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, MediaType, MediaSource


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print a PCL5 test file with media source command specified with tray3 and ensure PDL is processing the job with tray3
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-183335
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:Tray3.prn=3310656b796a1c221d51b6b7c9794cbcb5544e45b17100f0c702b36d39a84218
    +test_classification:System
    +name: test_pdl_intent_pcl5_mediasource_tray3_1page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pdl_intent_pcl5_mediasource_tray3_1page
        +guid:2cc608b0-b586-4183-aaf3-7dc6435aa864
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & MediaInputInstalled=Tray3 & MediaSizeSupported=na_letter_8.5x11in

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_intent_pcl5_mediasource_tray3_1page(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_tray_supported('tray-3') and tray.is_size_supported('na_letter_8.5x11in', 'tray-3'):
        tray.configure_tray('tray-3', 'na_letter_8.5x11in', 'stationery')
        printjob.print_verify('3310656b796a1c221d51b6b7c9794cbcb5544e45b17100f0c702b36d39a84218')
        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 1)
        outputverifier.verify_collated_copies(Intents.printintent, 1)
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
        outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        outputverifier.verify_media_source(Intents.printintent, MediaSource.tray3)
        outputsaver.save_output()
        outputsaver.operation_mode('NONE')
        tray.reset_trays()
