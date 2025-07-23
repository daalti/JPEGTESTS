import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-Orientation-8.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-Orientation-8.pwg=914f30ffceeb8c10234eb36c7cfe5f8a2b7d09f7307ac1886bdf91200f0edbbc
    +name:test_pwg_cloud_print_orientation_8
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_orientation_8
        +guid:8baa8ae3-f7e6-4088-afbf-8d160e751c56
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_orientation_8(setup_teardown, printjob, outputsaver):
    printjob.print_verify('914f30ffceeb8c10234eb36c7cfe5f8a2b7d09f7307ac1886bdf91200f0edbbc', 'FAILED')
    outputsaver.save_output()
