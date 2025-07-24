import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using AlphaDiskMacro.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:AlphaDiskMacro.pcl=8697cbace1436bcf21fe7edbbb8840f6d15e9e3b2106f76fab544f4929d61760
    +test_classification:System
    +name: test_pcl5_testfiles_misc_alphadiskmacro
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_misc_alphadiskmacro
        +guid:d9883f44-5a03-48e6-9a88-d9b87910af7b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_alphadiskmacro(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8697cbace1436bcf21fe7edbbb8840f6d15e9e3b2106f76fab544f4929d61760', timeout=600)
    outputsaver.save_output()
