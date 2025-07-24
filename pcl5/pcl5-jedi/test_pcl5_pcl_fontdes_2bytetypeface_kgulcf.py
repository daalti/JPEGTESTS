import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kgulcf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kgulcf.obj=dc31ac8bb908f6b69fa9f682126d210998bbb4635e9a2abd752dcf2664f07848
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kgulcf
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kgulcf
        +guid:2a9ec7d8-1ad1-4c2c-b02b-370a49d8db30
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kgulcf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dc31ac8bb908f6b69fa9f682126d210998bbb4635e9a2abd752dcf2664f07848', timeout=600)
    outputsaver.save_output()
