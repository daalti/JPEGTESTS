import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using displayFunc.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:displayFunc.pcl=50b0b1197b88cc95d0127ed9db4c7d420a5c0a1cf092fd7819cf774e09d6a704
    +test_classification:System
    +name: test_pcl5_testfiles_misc_displayfunc
    +test:
        +title: test_pcl5_testfiles_misc_displayfunc
        +guid:189391c0-5f75-4597-838e-5e1e594ee7fd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_misc_displayfunc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('50b0b1197b88cc95d0127ed9db4c7d420a5c0a1cf092fd7819cf774e09d6a704', timeout=600)
    outputsaver.save_output()
