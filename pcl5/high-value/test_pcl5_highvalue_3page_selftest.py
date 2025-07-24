import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 3Page_selftest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-selftest.obj=2a71ca61424c6591c2cfb534e423cfe3fb8ecd0f3cd409ec8ec0064a880b3816
    +test_classification:System
    +name: test_pcl5_highvalue_3page_selftest
    +test:
        +title: test_pcl5_highvalue_3page_selftest
        +guid:902ed05b-dbeb-4d55-b9dd-d9a0a313692b
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

def test_pcl5_highvalue_3page_selftest(setup_teardown, printjob, counters, outputsaver):
    printjob.print_verify('2a71ca61424c6591c2cfb534e423cfe3fb8ecd0f3cd409ec8ec0064a880b3816')
    outputsaver.save_output()
