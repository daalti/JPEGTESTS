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
    +external_files:c5.pcl=d2c065f69e2b35312fefd6dc81626940cab1f72820034b9468a6adfaebe477c2
    +name:test_pcl5_c5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_c5
        +guid:21783017-1de8-43bd-b322-f35ee169a938
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_c5(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('iso_c5_162x229mm','tray-1'):
        tray.configure_tray('tray-1', 'iso_c5_162x229mm', 'any')
    printjob.print_verify_multi('d2c065f69e2b35312fefd6dc81626940cab1f72820034b9468a6adfaebe477c2')
    outputsaver.save_output()  