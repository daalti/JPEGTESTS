import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using patRefPt.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:patRefPt.pcl=e7d3035dbfe0ae42b82168a9cffa80f923ce9ba5ff789b0d95d0c228d1f29ea0
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_patrefpt
    +test:
        +title: test_pcl5_testfiles_pattern_patrefpt
        +guid:30d6e957-2b9f-41f2-bb93-8379f7260c0a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_patrefpt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e7d3035dbfe0ae42b82168a9cffa80f923ce9ba5ff789b0d95d0c228d1f29ea0', timeout=600)
    outputsaver.save_output()
