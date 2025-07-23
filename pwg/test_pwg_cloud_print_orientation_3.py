import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-Orientation-3.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-Orientation-3.pwg=0fb7aa66b80a8a3ea9c135bc3c8ac18027e782e93949c84e67aa02482be59009
    +name:test_pwg_cloud_print_orientation_3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_orientation_3
        +guid:a86b7c80-4fd7-4a7d-9b3b-7971bf9ca769
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_orientation_3(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0fb7aa66b80a8a3ea9c135bc3c8ac18027e782e93949c84e67aa02482be59009', 'FAILED')
    outputsaver.save_output()
