import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kbatcf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kbatcf.obj=4a8469deea4e4db35f0891940821627dcc3792f1dec79bd42401ee160b98e853
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kbatcf
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kbatcf
        +guid:d6caf0c2-d506-454d-b669-3b2caafb006d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kbatcf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4a8469deea4e4db35f0891940821627dcc3792f1dec79bd42401ee160b98e853', timeout=600)
    outputsaver.save_output()
