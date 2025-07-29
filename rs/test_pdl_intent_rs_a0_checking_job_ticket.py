import pytest
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, MediaType, MediaSource

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple print from a rasterstream (a3.rs) file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-152360
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:a3.rs=b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617
    +name:test_pdl_intent_rs_a0_checking_job_ticket
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_rs_a0_checking_job_ticket
        +guid:e5ef84ea-76c6-4b17-a638-9aaea67aabea
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=RasterStreamICF & MediaInputInstalled=ROLL1 & MediaSizeSupported=iso_a0_841x1189mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_rs_a0_checking_job_ticket(setup_teardown, printjob, outputsaver, outputverifier, tray):
    if tray.is_size_supported('iso_a0_841x1189mm', 'roll-1'):
        tray.configure_tray('roll-1', 'iso_a0_841x1189mm', 'stationery')

    printjob.print_verify('b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 1)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a0)
    outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.roll1)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_resolution(Intents.printintent, 600)
    outputverifier.outputsaver.operation_mode('NONE')
    tray.reset_trays()
