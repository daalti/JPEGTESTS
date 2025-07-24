import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 12Page_rq.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:12Page-rq.obj=c2c253b52173d5f1fdf88484a92ccd53a179f4f1110b31c4d6ad1a821e1a5ce6
    +test_classification:System
    +name: test_pcl5_highvalue_12page_rq
    +test:
        +title: test_pcl5_highvalue_12page_rq
        +guid:c8c68dc1-729c-4731-acf2-560f0d91aa8c
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

def test_pcl5_highvalue_12page_rq(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c2c253b52173d5f1fdf88484a92ccd53a179f4f1110b31c4d6ad1a821e1a5ce6', timeout=300)
    outputsaver.save_output()
