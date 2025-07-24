import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using gpri_1.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:700
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:gpri_1.obj=4ed43cc07955a637a61f509540d6ec5b86512b8329a598b8fa026eba83df9c57
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_gpri_1
    +test:
        +title: test_pcl5_pcl_font_feature_gpri_1
        +guid:8d79ff1e-63f6-4849-b904-b0f36e4d1839
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_gpri_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4ed43cc07955a637a61f509540d6ec5b86512b8329a598b8fa026eba83df9c57', timeout=700)
    outputsaver.save_output()
