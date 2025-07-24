import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 6Page_pitchm1.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:6Page-pitchm1.obj=56a0381d7c8d2e947765c6df4da35a42413b02c7a2925606cc2c95ad62d8f41b
    +test_classification:System
    +name: test_pcl5_lowvaluenew_6page_pitchm1
    +test:
        +title: test_pcl5_lowvaluenew_6page_pitchm1
        +guid:97384f8c-4db7-4fc9-b0b7-025a3f65be9e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_6page_pitchm1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('56a0381d7c8d2e947765c6df4da35a42413b02c7a2925606cc2c95ad62d8f41b', timeout=600)
    outputsaver.save_output()
