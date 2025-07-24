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
    +external_files:monarch.pcl=02c197a1c0beb8fa2ede54d3675a3476634434b377bfdff5a3979e76194bd057
    +name:test_pcl5_monarch
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_monarch
        +guid:7905c208-8504-4bbe-8706-d8f4080bfb39
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_monarch(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('na_monarch_3.875x7.5in','tray-1'):
        tray.configure_tray('tray-1', 'na_monarch_3.875x7.5in', 'any')
    printjob.print_verify_multi('02c197a1c0beb8fa2ede54d3675a3476634434b377bfdff5a3979e76194bd057')
    outputsaver.save_output() 