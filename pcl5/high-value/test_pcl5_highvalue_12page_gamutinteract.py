import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 12Page_gamutinteract.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:12Page-gamutinteract.obj=1c7d02a6a1fcd33600e3cd2e845446fb2d78d208b1fb5f39058cd81d9d2fa207
    +test_classification:System
    +name: test_pcl5_highvalue_12page_gamutinteract
    +test:
        +title: test_pcl5_highvalue_12page_gamutinteract
        +guid:8a43a0aa-2c28-4f0a-ba46-fbf396a2dff5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_12page_gamutinteract(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1c7d02a6a1fcd33600e3cd2e845446fb2d78d208b1fb5f39058cd81d9d2fa207', timeout=300)
    outputsaver.save_output()
