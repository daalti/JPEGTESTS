import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only whx bitmap page-2 from *PwgPhOnly-WxHBitmap-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-WxHBitmap-2.pwg=81ed7378ba8a7b6dc9ff826806922108b998c4d0e6034bdb0333c1d3aeee3fdb
    +name:test_pwg_ph_only_wxh_bitmap_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_wxh_bitmap_2
        +guid:3f122530-2e63-4cd1-b7e8-b3f77c16c678
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_wxh_bitmap_2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('81ed7378ba8a7b6dc9ff826806922108b998c4d0e6034bdb0333c1d3aeee3fdb', 'FAILED')
    outputsaver.save_output()

    logging.info("PWG Ph Only Whx Bitmap-2 - Print job completed successfully!")
