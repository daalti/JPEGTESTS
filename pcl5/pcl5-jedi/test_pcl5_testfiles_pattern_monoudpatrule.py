import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using monoUDPatRule.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:monoUDPatRule.pcl=1394760f48cb706d9c6ecad0da26016e7c11866454426c476a8c871eb705d391
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_monoudpatrule
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_pattern_monoudpatrule
        +guid:ac3874f5-f675-434c-a995-83fe294a3564
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_monoudpatrule(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1394760f48cb706d9c6ecad0da26016e7c11866454426c476a8c871eb705d391', timeout=600)
    outputsaver.save_output()
