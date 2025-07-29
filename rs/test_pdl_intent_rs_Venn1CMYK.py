import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, MediaType, MediaSource

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job of file Venn1CMYK.rs **
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-152360
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Venn1CMYK.rs=2460d37ca59f6d731cd69e69f62e3f50846a1c7b80859d8172780a4f40064693
    +test_classification:System
    +name:test_pdl_intent_rs_Venn1CMYK
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_rs_Venn1CMYK
        +guid:44c9b698-13a2-42ac-9e73-cefb9c03df99
        +dut:
            +type:Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF & MediaInputInstalled=ROLL2 & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_intent_rs_Venn1CMYK(setup_teardown, printjob, outputsaver, tray, outputverifier):
    if tray.is_size_supported('iso_a1_594x841mm', 'roll-2'):
        tray.configure_tray('roll-2', 'iso_a1_594x841mm', 'stationery')

    printjob.print_verify('2460d37ca59f6d731cd69e69f62e3f50846a1c7b80859d8172780a4f40064693')
    logging.info("RS Venn1CMYK - Print job completed successfully")
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a1)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.roll2)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputverifier.outputsaver.operation_mode('NONE')
    tray.reset_trays()

