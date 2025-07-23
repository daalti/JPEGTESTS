import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgPhOnly-MediaSelectByPageSize-4_old.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-MediaSelectByPageSize-4_old.pwg=68d994258f78a425881a2f8c5c2267a8b2c81891bfcda60436049ad27c08a7ff
    +name:test_pwg_ph_only_media_select_by_page_size_4_old
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_media_select_by_page_size_4_old
        +guid:3820acb1-1a7e-4f5d-aa1a-71cfef004850
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_media_select_by_page_size_4_old(setup_teardown, printjob, outputsaver):
    printjob.print_verify('68d994258f78a425881a2f8c5c2267a8b2c81891bfcda60436049ad27c08a7ff', 'FAILED', timeout=180)
    outputsaver.save_output()
