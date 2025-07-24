import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 1Page_vecrastx.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-vecrastx.obj=4d1d4356b7babba5b2760663ef9b61b407aa4fff56d58c388ad2b0577c1af505
    +test_classification:System
    +name: test_pcl5_basicfunctionality_1page_vecrastx
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_1page_vecrastx
        +guid:2066c9be-ab2b-4990-8b50-fe7e8f0b3884
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_basicfunctionality_1page_vecrastx(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4d1d4356b7babba5b2760663ef9b61b407aa4fff56d58c388ad2b0577c1af505')
    outputsaver.save_output()
