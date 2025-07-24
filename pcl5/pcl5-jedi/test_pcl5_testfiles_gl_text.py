import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using text.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:text.pcl=97d0d67b686ece15b9384b3cf2f95e970ddf88a9d2c9f7e771352864413b66ea
    +test_classification:System
    +name: test_pcl5_testfiles_gl_text
    +test:
        +title: test_pcl5_testfiles_gl_text
        +guid:e4515e6a-5204-4831-9abc-36c319a39ab5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_text(setup_teardown, printjob, outputsaver):
    printjob.print_verify('97d0d67b686ece15b9384b3cf2f95e970ddf88a9d2c9f7e771352864413b66ea', timeout=600)
    outputsaver.save_output()
