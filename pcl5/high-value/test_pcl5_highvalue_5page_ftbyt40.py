import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 5Page_ftbyt40.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-ftbyt40.obj=a330f59fd2586cc3a7a593c73e1b4762437374dfe19cca55dc2f0264880f0b1c
    +test_classification:System
    +name: test_pcl5_highvalue_5page_ftbyt40
    +test:
        +title: test_pcl5_highvalue_5page_ftbyt40
        +guid:ac6889a5-6023-4e91-bbf0-5ddfbef514c3
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

def test_pcl5_highvalue_5page_ftbyt40(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a330f59fd2586cc3a7a593c73e1b4762437374dfe19cca55dc2f0264880f0b1c', timeout=600)
    outputsaver.save_output()
