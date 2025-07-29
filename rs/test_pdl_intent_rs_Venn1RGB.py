import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, MediaType, MediaSource

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job of file Venn1RGB.rs **
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-152360
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Venn1RGB.rs=e4b093935481c7ec9e428194a9c7fa475558e18104bb66dfdd4736b81906f3a5
    +test_classification:System
    +name:test_pdl_intent_rs_Venn1RGB
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_rs_Venn1RGB
        +guid:2fd1faf5-6cf0-435a-bea4-88b01cbfe564
        +dut:
            +type:Simulator
            +configuration:PrintEngineType=Maia & DocumentFormat=RasterStreamICF & MediaInputInstalled=ROLL1 & MediaSizeSupported=iso_a2_420x594mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pdl_intent_rs_Venn1RGB(setup_teardown, printjob, outputsaver, outputverifier, tray):
    if tray.is_size_supported('iso_a2_420x594mm', 'roll-1'):
        tray.configure_tray('roll-1', 'iso_a2_420x594mm', 'stationery')

    printjob.print_verify('e4b093935481c7ec9e428194a9c7fa475558e18104bb66dfdd4736b81906f3a5')
    logging.info("RS Venn1RGB - Print job completed successfully")
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a2)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.roll1)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputsaver.save_output()
    outputverifier.outputsaver.operation_mode('NONE')
    tray.reset_trays()
