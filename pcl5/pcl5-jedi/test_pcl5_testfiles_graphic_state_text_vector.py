import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using TextVector.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:TextVector.pcl=29e9f2305d9cc6c5c8cbed46090e4f1b264759d5d6280ddb1bc5e978a56bc0c6
    +test_classification:System
    +name: test_pcl5_testfiles_graphic_state_text_vector
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_graphic_state_text_vector
        +guid:a9599af1-8590-4b83-9d1d-e9ae7b2983bf
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_graphic_state_text_vector(setup_teardown, printjob, outputsaver):
    printjob.print_verify('29e9f2305d9cc6c5c8cbed46090e4f1b264759d5d6280ddb1bc5e978a56bc0c6', timeout=600)
    outputsaver.save_output()
