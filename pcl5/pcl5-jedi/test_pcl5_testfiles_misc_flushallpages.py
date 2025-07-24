import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using flushAllPages.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:flushAllPages.pcl=ef828569932bf490a418b7a753ca1311d52ab5c7c86dd08ffa7c0f78384b12c4
    +test_classification:System
    +name: test_pcl5_testfiles_misc_flushallpages
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_misc_flushallpages
        +guid:d2fd2c07-c78d-451f-87e3-45465651e180
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_flushallpages(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ef828569932bf490a418b7a753ca1311d52ab5c7c86dd08ffa7c0f78384b12c4', timeout=600)
    outputsaver.save_output()
