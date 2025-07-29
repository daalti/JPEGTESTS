import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, MediaType, MediaSource

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job of a rasterstream file tower_a3.rs
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-152360
    +timeout:300
    +asset:LFP
    +test_framework:TUF
    +external_files:tower_a3.rs=b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617
    +test_classification:System
    +name:test_pdl_intent_rs_tower_a3
    +test:
        +title:test_pdl_intent_rs_tower_a3
        +guid:3f43f7a1-c4df-49cc-95f0-d207ec1b033d
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF & MediaInputInstalled=ROLL1 & MediaSizeSupported=custom

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_rs_tower_a3(setup_teardown, printjob, outputsaver, outputverifier, tray):

    printjob.print_verify('b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617', timeout=300)
    logging.info("tower_a3.rs - Print job completed successfully")
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.roll1)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputverifier.outputsaver.operation_mode('NONE')
    tray.reset_trays()

