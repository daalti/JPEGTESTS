import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using transparentData.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:transparentData.pcl=dbeed7b1f6008c0b65d79b485301e4207e88d12132dbe6c68a6264a868a2c999
    +test_classification:System
    +name: test_pcl5_testfiles_misc_transparentdata
    +test:
        +title: test_pcl5_testfiles_misc_transparentdata
        +guid:3632cdf0-7894-4926-a501-a176d21e271d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_transparentdata(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dbeed7b1f6008c0b65d79b485301e4207e88d12132dbe6c68a6264a868a2c999', timeout=600)
    outputsaver.save_output()
