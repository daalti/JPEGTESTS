import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using hpglpclcap.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:hpglpclcap.pcl=bba3aa3a2e28d83a95ad4c869532af192b8e4ea202ccb017bd453a9969cad8a2
    +test_classification:System
    +name: test_pcl5_testfiles_graphic_state_hpglpclcap
    +test:
        +title: test_pcl5_testfiles_graphic_state_hpglpclcap
        +guid:9ac85af6-80e1-49e8-a01d-32621fc6f153
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_graphic_state_hpglpclcap(setup_teardown, printjob, outputsaver):
    printjob.print_verify('bba3aa3a2e28d83a95ad4c869532af192b8e4ea202ccb017bd453a9969cad8a2', timeout=600)
    outputsaver.save_output()
