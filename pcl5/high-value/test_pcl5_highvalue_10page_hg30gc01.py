import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 10Page_hg30gc01.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:10Page-hg30gc01.obj=9e38d25f543a21176fb91e6543f8aba6aec6dc0d4526ef0c3989cf38e2a0a4b1
    +test_classification:System
    +name: test_pcl5_highvalue_10page_hg30gc01
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_10page_hg30gc01
        +guid:aa2a4554-65ef-4112-aa35-2db24f210910
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_highvalue_10page_hg30gc01(setup_teardown, printjob, outputsaver):
    # This file create 4 jobs with total of 9 pages.
    printjob.print_verify_multi('9e38d25f543a21176fb91e6543f8aba6aec6dc0d4526ef0c3989cf38e2a0a4b1', timeout=600, expected_jobs=4)
    outputsaver.save_output()
