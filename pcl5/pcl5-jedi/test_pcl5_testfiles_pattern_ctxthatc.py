import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ctxthatc.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ctxthatc.pcl=9cc3214827da72b0de36660340e9224a4e418f8db63363233a0b6727849f2954
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_ctxthatc
    +test:
        +title: test_pcl5_testfiles_pattern_ctxthatc
        +guid:8ec908cd-51ed-46f9-9d53-a2f6928a3f45
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_ctxthatc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9cc3214827da72b0de36660340e9224a4e418f8db63363233a0b6727849f2954', timeout=600)
    outputsaver.save_output()
