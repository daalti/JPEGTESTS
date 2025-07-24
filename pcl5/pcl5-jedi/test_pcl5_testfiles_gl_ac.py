import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ac.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ac.pcl=6465e086a5f24722da1d976fd6b8c1f04922e960a388adb4e5e24cc72e6527a9
    +test_classification:System
    +name: test_pcl5_testfiles_gl_ac
    +test:
        +title: test_pcl5_testfiles_gl_ac
        +guid:6bfd7ec4-512e-4524-b63d-21cbdff410e8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_ac(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6465e086a5f24722da1d976fd6b8c1f04922e960a388adb4e5e24cc72e6527a9', timeout=600)
    outputsaver.save_output()
