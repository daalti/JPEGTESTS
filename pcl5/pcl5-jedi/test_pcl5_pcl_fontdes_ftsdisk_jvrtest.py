import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jvrtest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jvrtest.obj=60a2ccef2153759531d8d632655bfded50432ebf2bbcbb4c2de08b8026de66ba
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_jvrtest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_jvrtest
        +guid:56d8db8f-a343-4333-b769-ddba563067fa
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_jvrtest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('60a2ccef2153759531d8d632655bfded50432ebf2bbcbb4c2de08b8026de66ba', timeout=600)
    outputsaver.save_output()
