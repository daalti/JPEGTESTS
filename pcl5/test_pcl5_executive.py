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
    +external_files:executive.pcl=8c506918be57ab4d038b3cf3429f6b5fd64c3a0edba8f0f206455cc0e7ec8db0
    +name:test_pcl5_executive
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_executive
        +guid:c74da291-4866-4c8c-a1c7-12ab51483a06
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_executive(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('na_executive_7.25x10.5in','tray-1'):
        tray.configure_tray('tray-1', 'na_executive_7.25x10.5in', 'any')
    printjob.print_verify_multi('8c506918be57ab4d038b3cf3429f6b5fd64c3a0edba8f0f206455cc0e7ec8db0')
    outputsaver.save_output()