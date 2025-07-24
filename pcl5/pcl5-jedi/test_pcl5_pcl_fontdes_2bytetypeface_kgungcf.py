import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kgungcf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kgungcf.obj=7b709ae51ba0831a8db5494258467d55b0933d076e1c9f40a2c5ed1b586a0bb7
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kgungcf
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kgungcf
        +guid:d9440659-2b1b-4adc-930d-8d27ef0a91d4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kgungcf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7b709ae51ba0831a8db5494258467d55b0933d076e1c9f40a2c5ed1b586a0bb7', timeout=600)
    outputsaver.save_output()
