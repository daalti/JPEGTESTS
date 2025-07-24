import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using multijob.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:multijob.pcl=4e05510cc56a97da530049322766594ea6ba0a29a5707f3912cac06672a71c5a
    +test_classification:System
    +name: test_pcl5_testfiles_graphic_state_multijob
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_graphic_state_multijob
        +guid:35219f25-f1dc-47df-b399-47b97744b423
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_graphic_state_multijob(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4e05510cc56a97da530049322766594ea6ba0a29a5707f3912cac06672a71c5a', timeout=600)
    outputsaver.save_output()
