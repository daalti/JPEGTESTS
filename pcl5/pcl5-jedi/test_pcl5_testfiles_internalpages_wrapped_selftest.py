import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using wrapped_selftest.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:wrapped_selftest.pcl=4eedc40a6db47c313d22bd5a27bc22a1f83ee0cacad51d284834a38e1d4dbef2
    +test_classification:System
    +name: test_pcl5_testfiles_internalpages_wrapped_selftest
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_internalpages_wrapped_selftest
        +guid:922c4a7d-3eab-4a6b-8f99-f6090025c063
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_internalpages_wrapped_selftest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4eedc40a6db47c313d22bd5a27bc22a1f83ee0cacad51d284834a38e1d4dbef2', timeout=600)
    outputsaver.save_output()
