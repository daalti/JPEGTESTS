import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-MediaSelectByPageSize-1.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-MediaSelectByPageSize-1.pwg=597eedc2a441e20568af95325af85a182f06d496c851092703dfd3b9a8d6175d
    +name:test_pwg_cloud_print_media_select_by_page_size_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_media_select_by_page_size_1
        +guid:4fe8386a-facf-4c34-b887-b2f76960701a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_media_select_by_page_size_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('597eedc2a441e20568af95325af85a182f06d496c851092703dfd3b9a8d6175d')
    outputsaver.save_output()
