import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using ew.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ew.pcl=44cb8887e69748d5e14073396d55a880ebb56280e39c41949eda28af1b742637
    +test_classification:System
    +name: test_pcl5_testfiles_gl_ew
    +test:
        +title: test_pcl5_testfiles_gl_ew
        +guid:764247b9-1b6e-4960-8278-f72d1d6e3539
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_ew(setup_teardown, printjob, outputsaver):
    printjob.print_verify('44cb8887e69748d5e14073396d55a880ebb56280e39c41949eda28af1b742637', timeout=600)
    outputsaver.save_output()
