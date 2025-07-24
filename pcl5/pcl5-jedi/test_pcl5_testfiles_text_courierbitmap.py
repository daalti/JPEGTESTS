import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using CourierBitmap.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:CourierBitmap.pcl=ed55efa3b4ed41336d91b281838991653dafa6d4509d5db6335c90db0263b9b4
    +test_classification:System
    +name: test_pcl5_testfiles_text_courierbitmap
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_text_courierbitmap
        +guid:fb8b4424-1d3e-4edb-9aba-509722546fa5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_text_courierbitmap(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ed55efa3b4ed41336d91b281838991653dafa6d4509d5db6335c90db0263b9b4', timeout=600)
    outputsaver.save_output()
