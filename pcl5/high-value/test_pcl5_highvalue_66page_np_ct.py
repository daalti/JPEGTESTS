import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 66Page_np_ct.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:66Page-np_ct.obj=ae9f0a34e8494739fa50df8ea429464affbd8b6007f162a36453a75b27ff5c9c
    +test_classification:System
    +name: test_pcl5_highvalue_66page_np_ct
    +test:
        +title: test_pcl5_highvalue_66page_np_ct
        +guid:3b1d4c64-9702-4933-a903-780d53260f2f
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

def test_pcl5_highvalue_66page_np_ct(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ae9f0a34e8494739fa50df8ea429464affbd8b6007f162a36453a75b27ff5c9c', timeout=900)
    outputsaver.save_output()
