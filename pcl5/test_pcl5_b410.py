import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464	
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:b410.pcl=4b15dc315247658a8bc18be459bd93afbf19e3d106a67d5eb5d1fc98ba7facf5
    +name:test_pcl5_b410
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_b410
        +guid:06f7ab7d-6ae0-43f0-8df1-a0b370e11c23
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_b410(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('jis_b5_182x257mm','tray-1'):
        tray.configure_tray('tray-1', 'jis_b5_182x257mm', 'any')
    printjob.print_verify_multi('4b15dc315247658a8bc18be459bd93afbf19e3d106a67d5eb5d1fc98ba7facf5')
    outputsaver.save_output()
