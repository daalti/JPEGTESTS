import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tittest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tittest.obj=79668b60e181f1915b04016ffc2c2aec9a4903064195e040c5669bb27591a521
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_tittest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_tittest
        +guid:a16ac821-488e-4632-bdba-ed2c952c247c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_tittest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('79668b60e181f1915b04016ffc2c2aec9a4903064195e040c5669bb27591a521', timeout=600)
    outputsaver.save_output()
