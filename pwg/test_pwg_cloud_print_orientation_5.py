import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-Orientation-5.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-Orientation-5.pwg=a87e49b791aefb8b1971f4f889d51e027dce797e88438a4464189ac9512c1247
    +name:test_pwg_cloud_print_orientation_5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_orientation_5
        +guid:b2116ec0-abf6-4307-8d2e-d8f0166c4e12
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_orientation_5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a87e49b791aefb8b1971f4f889d51e027dce797e88438a4464189ac9512c1247', 'FAILED')
    outputsaver.save_output()
