import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ttest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ttest.obj=a17715f682a4fc3242a36d33c27776a973c35d37e0099721d52676a7c19b5405
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_ttest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_ttest
        +guid:e49aacb8-eeee-488d-8253-7bdf83ba6414
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_ttest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a17715f682a4fc3242a36d33c27776a973c35d37e0099721d52676a7c19b5405', timeout=600)
    outputsaver.save_output()
