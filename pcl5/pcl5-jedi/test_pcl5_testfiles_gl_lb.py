import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using lb.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:lb.pcl=f49e46f5a01d6b2d164e17089a54ecd00369f3f2e2d68ea5d34f3b5b114e3218
    +test_classification:System
    +name: test_pcl5_testfiles_gl_lb
    +test:
        +title: test_pcl5_testfiles_gl_lb
        +guid:8ed1a57a-9f61-40f6-8523-e96dd54a7ca9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_lb(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f49e46f5a01d6b2d164e17089a54ecd00369f3f2e2d68ea5d34f3b5b114e3218', timeout=600)
    outputsaver.save_output()
