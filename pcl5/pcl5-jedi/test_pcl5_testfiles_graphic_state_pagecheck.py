import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using PageCheck.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:PageCheck.pcl=0c8699a59acb1766e4fc39930efcf741e43a5d140467c333c3c043bab4fd3394
    +test_classification:System
    +name: test_pcl5_testfiles_graphic_state_pagecheck
    +test:
        +title: test_pcl5_testfiles_graphic_state_pagecheck
        +guid:caf02db5-2891-4fdc-8c8e-2966bd84b706
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_graphic_state_pagecheck(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0c8699a59acb1766e4fc39930efcf741e43a5d140467c333c3c043bab4fd3394', timeout=600)
    outputsaver.save_output()
