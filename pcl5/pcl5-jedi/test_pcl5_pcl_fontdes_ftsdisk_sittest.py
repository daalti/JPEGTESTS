import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using sittest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sittest.obj=4ec8ed9d228edfba4c79657840fd680d24c8c52e58e7fc099d70160bff5aa1b7
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_sittest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_sittest
        +guid:dce92a6f-edd7-43a3-afd6-ff6f7e2089b6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_sittest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4ec8ed9d228edfba4c79657840fd680d24c8c52e58e7fc099d70160bff5aa1b7', timeout=600)
    outputsaver.save_output()
