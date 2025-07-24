import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 174Page_latin25.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:174Page-latin25.obj=1b1d9df23e36c7c6ad52107e356713b1e0fa8ae46c4f7591c84ea57b5cfb653a
    +test_classification:System
    +name: test_pcl5_highvalue_174page_latin25
    +test:
        +title: test_pcl5_highvalue_174page_latin25
        +guid:c0333772-96ad-403e-8f72-bc1979f246bc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:4000
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_174page_latin25(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1b1d9df23e36c7c6ad52107e356713b1e0fa8ae46c4f7591c84ea57b5cfb653a', timeout=3600)
    outputsaver.save_output()
