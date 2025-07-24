import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using UnCollatedCopies2.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:UnCollatedCopies2.pcl=5b1d890f8297053b0a407aa4da7ebfb4a3643c2d8a62ef27ac8d3583e53916c0
    +test_classification:System
    +name: test_pcl5_testfiles_uncollatedcopies2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_uncollatedcopies2
        +guid:33f38e67-a2b7-45c8-93dd-3f7bcd7ce435
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_uncollatedcopies2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5b1d890f8297053b0a407aa4da7ebfb4a3643c2d8a62ef27ac8d3583e53916c0', timeout=600)
    outputsaver.save_output()
