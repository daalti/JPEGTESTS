import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-Orientation-9.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-Orientation-9.pwg=cdae98a174527d911696baed0fa8f7832a786104f07539dd05013f917b3127d1
    +name:test_pwg_cloud_print_orientation_9
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_orientation_9
        +guid:cbf5f2fe-dfb9-4b40-9eca-96ec47681149
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_orientation_9(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cdae98a174527d911696baed0fa8f7832a786104f07539dd05013f917b3127d1', 'FAILED')
    outputsaver.save_output()
