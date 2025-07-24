import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ctxtusr.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ctxtusr.pcl=aa90b1c61d85b81ebeaffe6384c8e2ed018c1abb2b2c4cf36853241b7e7a8d35
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_ctxtusr
    +test:
        +title: test_pcl5_testfiles_pattern_ctxtusr
        +guid:c1258210-6aff-4cc5-989f-e64094f219a4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_ctxtusr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('aa90b1c61d85b81ebeaffe6384c8e2ed018c1abb2b2c4cf36853241b7e7a8d35', timeout=600)
    outputsaver.save_output()
