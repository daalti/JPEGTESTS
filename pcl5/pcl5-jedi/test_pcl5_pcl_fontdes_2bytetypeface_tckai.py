import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tckai.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tckai.obj=4b969c90b9e8b787fc13669e65ac9c5af7c7f666d59e4ed5d4394416df819145
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_tckai
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_tckai
        +guid:c6e47c7d-c349-4442-b5ae-29fc4275dab1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_tckai(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4b969c90b9e8b787fc13669e65ac9c5af7c7f666d59e4ed5d4394416df819145', timeout=600)
    outputsaver.save_output()
