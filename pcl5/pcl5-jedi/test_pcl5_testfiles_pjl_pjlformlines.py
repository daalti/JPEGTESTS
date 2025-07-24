import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using pjlformlines.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:pjlformlines.pcl=f6e2b8d9c90cf3a28f8bbc8c78a02446ad3a5ec908779330f2547128b4da014b
    +test_classification:System
    +name: test_pcl5_testfiles_pjl_pjlformlines
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_pjl_pjlformlines
        +guid:f9d6d1cc-a058-4f5c-96cf-e5c47baf9e7f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pjl_pjlformlines(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f6e2b8d9c90cf3a28f8bbc8c78a02446ad3a5ec908779330f2547128b4da014b', timeout=600)
    outputsaver.save_output()
