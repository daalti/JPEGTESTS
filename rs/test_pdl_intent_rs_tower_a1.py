import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, MediaType, MediaSource

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple print from a rasterstream tower_a1.rs file.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-152360
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:tower_a1.rs=abfae6b4e8b5597dd712c14e210626b3fc3f13e040610e704cd0cc2d760a92ab
    +test_classification:System
    +name:test_pdl_intent_rs_tower_a1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_rs_tower_a1
        +guid:b0a6fa8b-83d2-42a0-b52f-40b13c75268f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=RasterStreamICF & MediaInputInstalled=ROLL2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_rs_tower_a1(setup_teardown, printjob, outputsaver, outputverifier, tray):
    if tray.is_size_supported('iso_a1_594x841mm', 'roll-1'):
        tray.configure_tray('roll-1', 'iso_a1_594x841mm', 'stationery')

    printjob.print_verify('abfae6b4e8b5597dd712c14e210626b3fc3f13e040610e704cd0cc2d760a92ab', timeout=300)
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.roll2)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputverifier.outputsaver.operation_mode('NONE')
    tray.reset_trays()
