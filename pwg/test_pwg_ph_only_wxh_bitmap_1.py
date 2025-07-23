import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only whx bitmap page-1 from *PwgPhOnly-WxHBitmap-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-WxHBitmap-1.pwg=acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c
    +name:test_pwg_ph_only_wxh_bitmap_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_wxh_bitmap_1
        +guid:39047d8e-eb74-496b-b2e1-991438378de4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_wxh_bitmap_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c')
    outputsaver.save_output()

    logging.info("PWG Ph Only Whx Bitmap-1 - Print job completed successfully!")
