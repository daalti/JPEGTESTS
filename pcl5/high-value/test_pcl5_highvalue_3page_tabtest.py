import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 3Page_tabtest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-tabtest.obj=764ecdf44f54bcbbb22affd40344501ab290cd4dea77cf12570203edd79ea890
    +test_classification:System
    +name: test_pcl5_highvalue_3page_tabtest
    +test:
        +title: test_pcl5_highvalue_3page_tabtest
        +guid:30d49b0b-7784-486c-a6cd-3580d83140be
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

def test_pcl5_highvalue_3page_tabtest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('764ecdf44f54bcbbb22affd40344501ab290cd4dea77cf12570203edd79ea890')
    outputsaver.save_output()
