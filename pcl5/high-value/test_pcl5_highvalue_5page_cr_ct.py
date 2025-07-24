import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 5Page_cr_ct.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-cr_ct.obj=18be5b39f752d958aad299cc0962394dc8ffc6203192cf1c5f533f35422e9776
    +test_classification:System
    +name: test_pcl5_highvalue_5page_cr_ct
    +test:
        +title: test_pcl5_highvalue_5page_cr_ct
        +guid:8f66eb46-8d1a-479c-af9c-04d5589f950c
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

def test_pcl5_highvalue_5page_cr_ct(setup_teardown, printjob, outputsaver):
    printjob.print_verify('18be5b39f752d958aad299cc0962394dc8ffc6203192cf1c5f533f35422e9776', timeout=600)
    outputsaver.save_output()
