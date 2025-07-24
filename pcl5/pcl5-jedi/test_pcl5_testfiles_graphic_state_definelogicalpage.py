import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using DefineLogicalPage.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:DefineLogicalPage.pcl=418d7e4cee8f66e8d3aa8621d97a83db21cc894fe1501c1d2018834f7c9501a8
    +test_classification:System
    +name: test_pcl5_testfiles_graphic_state_definelogicalpage
    +test:
        +title: test_pcl5_testfiles_graphic_state_definelogicalpage
        +guid:0aa8e1ae-4896-4f54-af9f-38abda2a19ae
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_graphic_state_definelogicalpage(setup_teardown, printjob, outputsaver):
    printjob.print_verify('418d7e4cee8f66e8d3aa8621d97a83db21cc894fe1501c1d2018834f7c9501a8', timeout=600)
    outputsaver.save_output()
