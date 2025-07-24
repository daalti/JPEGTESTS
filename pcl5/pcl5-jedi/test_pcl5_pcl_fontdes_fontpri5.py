import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fontpri5.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fontpri5.obj=7aa4e90fc2b60f30cbe8a6591b052d84ce60e43139d056e0a0045dc0467d9ab2
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_fontpri5
    +test:
        +title: test_pcl5_pcl_fontdes_fontpri5
        +guid:6d9500c6-3a73-4b24-86f0-3c6667f1d0dc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_fontpri5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7aa4e90fc2b60f30cbe8a6591b052d84ce60e43139d056e0a0045dc0467d9ab2', timeout=600)
    outputsaver.save_output()
