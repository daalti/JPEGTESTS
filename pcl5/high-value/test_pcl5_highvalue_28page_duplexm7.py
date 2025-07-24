import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 28Page_duplexm7.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:28Page-duplexm7.obj=3e5ae0625f3af962b0eba8a0c8019a1e403ec7c04e1a6131ddac4d828724382b
    +test_classification:System
    +name: test_pcl5_highvalue_28page_duplexm7
    +test:
        +title: test_pcl5_highvalue_28page_duplexm7
        +guid:1b46465c-fd66-4f3a-a9a1-f42ad7133dd2
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

def test_pcl5_highvalue_28page_duplexm7(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3e5ae0625f3af962b0eba8a0c8019a1e403ec7c04e1a6131ddac4d828724382b', timeout=600)
    outputsaver.save_output()
