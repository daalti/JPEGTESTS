import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-Orientation-6.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-Orientation-6.pwg=5338e09e0248feec28fe1380760beaff8356fdd9a639a09e5223164d520d77c6
    +name:test_pwg_cloud_print_orientation_6
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_orientation_6
        +guid:cd71f121-1758-4729-b6de-0855ddbaf6e2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_orientation_6(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5338e09e0248feec28fe1380760beaff8356fdd9a639a09e5223164d520d77c6', 'FAILED')
    outputsaver.save_output()
