import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PWG test using **PwgCloudPrint-Orientation-4.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-Orientation-4.pwg=b064f199414211c8dae7aca4cc6db8de9018b714cc4d1d140f093e4ff47a1452
    +name:test_pwg_cloud_print_orientation_4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_orientation_4
        +guid:2c12f228-38ef-460d-9934-0eac7a25fd7e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_orientation_4(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b064f199414211c8dae7aca4cc6db8de9018b714cc4d1d140f093e4ff47a1452', 'FAILED')
    outputsaver.save_output()
