import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using capmove.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:capmove.pcl=efb16cbc86b7bc4e8c7edac9c9b27e7d3a62c866c7c3bbe9cf1b2d2d46f04a99
    +test_classification:System
    +name: test_pcl5_testfiles_misc_capmove
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_misc_capmove
        +guid:3e4590ff-3da5-4f89-9ab7-8453b54a4112
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_capmove(setup_teardown, printjob, outputsaver):
    printjob.print_verify('efb16cbc86b7bc4e8c7edac9c9b27e7d3a62c866c7c3bbe9cf1b2d2d46f04a99', timeout=600)
    outputsaver.save_output()
