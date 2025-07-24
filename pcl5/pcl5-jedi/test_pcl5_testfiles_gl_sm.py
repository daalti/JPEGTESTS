import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using sm.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:sm.pcl=f617473d065be62224ac5edcfbdf8b2f7d4dcf403b3c214c859f1bd81f51617f
    +test_classification:System
    +name: test_pcl5_testfiles_gl_sm
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_gl_sm
        +guid:d8257bd2-be0d-4d64-93ee-62678bba1fd5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_sm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f617473d065be62224ac5edcfbdf8b2f7d4dcf403b3c214c859f1bd81f51617f', timeout=600)
    outputsaver.save_output()
