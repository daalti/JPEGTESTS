import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 2Page_trans.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2Page-trans.obj=bfa06b97cf793d157284d66e9f908363559faf1b63e85ebe6bed4bf333dedb4a
    +test_classification:System
    +name: test_pcl5_highvalue_2page_trans
    +test:
        +title: test_pcl5_highvalue_2page_trans
        +guid:c44a175e-0dbd-431f-8e60-a001f4c23273
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

def test_pcl5_highvalue_2page_trans(setup_teardown, printjob, outputsaver):
    printjob.print_verify('bfa06b97cf793d157284d66e9f908363559faf1b63e85ebe6bed4bf333dedb4a', timeout=600)
    outputsaver.save_output()
