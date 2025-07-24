import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using cusrdef.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cusrdef.pcl=b176b6b4e5be5e4bdd3efa65fbb77e65e1a75f3edccb2e3409ac01741a8bfda9
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_cusrdef
    +test:
        +title: test_pcl5_testfiles_pattern_cusrdef
        +guid:e1c9947c-3bd1-420f-9eee-e31e06ce0b60
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_cusrdef(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b176b6b4e5be5e4bdd3efa65fbb77e65e1a75f3edccb2e3409ac01741a8bfda9', timeout=600)
    outputsaver.save_output()
