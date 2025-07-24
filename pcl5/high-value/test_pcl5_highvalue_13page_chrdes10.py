import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 13Page_chrdes10.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:13Page-chrdes10.obj=f789427f274c02413ed90bbc6cddac7907178cccc1f22fe5c91cb683a3e6502a
    +test_classification:System
    +name: test_pcl5_highvalue_13page_chrdes10
    +test:
        +title: test_pcl5_highvalue_13page_chrdes10
        +guid:4407a1f7-b2bd-4380-a276-3e53da30c889
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

def test_pcl5_highvalue_13page_chrdes10(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f789427f274c02413ed90bbc6cddac7907178cccc1f22fe5c91cb683a3e6502a', timeout=300)
    outputsaver.save_output()
