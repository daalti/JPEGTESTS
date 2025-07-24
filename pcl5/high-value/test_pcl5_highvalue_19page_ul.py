import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 19Page_ul.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:19Page-ul.obj=c29473a0b7249603acb19651c42426281fab86895d696f2caf224685bf709a72
    +test_classification:System
    +name: test_pcl5_highvalue_19page_ul
    +test:
        +title: test_pcl5_highvalue_19page_ul
        +guid:634022a2-17bf-4c0e-8e1d-fab1140909e9
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

def test_pcl5_highvalue_19page_ul(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c29473a0b7249603acb19651c42426281fab86895d696f2caf224685bf709a72', timeout=600)
    outputsaver.save_output()
