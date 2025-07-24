import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using pitchm2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pitchm2.obj=72ad34b27ef34f1323fc4c8e8d0b5a8067b312346c30c1a4609b9c46717c4c6e
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_pitchm2
    +test:
        +title: test_pcl5_pcl_fontdes_pitchm2
        +guid:1d68ff0f-ec0f-4ee0-b6e1-b33809acdad2
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_pitchm2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('72ad34b27ef34f1323fc4c8e8d0b5a8067b312346c30c1a4609b9c46717c4c6e', timeout=600)
    outputsaver.save_output()
