import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using 2fonts.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2fonts.pcl=967f1d280dd4a7c294c2b603d6d06fc5b54cfd77c4d35987d795ade6720c930b
    +test_classification:System
    +name: test_pcl5_testfiles_gl_2fonts
    +test:
        +title: test_pcl5_testfiles_gl_2fonts
        +guid:2b158db8-8cdd-4b6a-9ff3-d19c0f88f9d6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_2fonts(setup_teardown, printjob, outputsaver):
    printjob.print_verify('967f1d280dd4a7c294c2b603d6d06fc5b54cfd77c4d35987d795ade6720c930b', timeout=600)
    outputsaver.save_output()
