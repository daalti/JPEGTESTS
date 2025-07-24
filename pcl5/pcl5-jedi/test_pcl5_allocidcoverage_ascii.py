import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 allocidcoverage using ascii.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:ascii.pcl=eaf547ccd8476ba5757e2cb3c58b6f8b5f0a93fc54d674d2a7b4288155a5f7e6
    +test_classification:System
    +name: test_pcl5_allocidcoverage_ascii
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_allocidcoverage_ascii
        +guid:5b993a08-1127-4e4d-9a9f-01a51b9e2c4d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_allocidcoverage_ascii(setup_teardown, printjob, outputsaver):
    printjob.print_verify('eaf547ccd8476ba5757e2cb3c58b6f8b5f0a93fc54d674d2a7b4288155a5f7e6', timeout=600)
    outputsaver.save_output()
