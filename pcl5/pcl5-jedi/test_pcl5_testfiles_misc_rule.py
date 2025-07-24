import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using rule.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:rule.pcl=dde6aa52fe1bc795aec93906ac6305161535680d5634c6ceedf23f46060a74c6
    +test_classification:System
    +name: test_pcl5_testfiles_misc_rule
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_misc_rule
        +guid:a86b8cf7-3953-49bb-8fbd-71127f0d57d1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_rule(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dde6aa52fe1bc795aec93906ac6305161535680d5634c6ceedf23f46060a74c6', timeout=600)
    outputsaver.save_output()
