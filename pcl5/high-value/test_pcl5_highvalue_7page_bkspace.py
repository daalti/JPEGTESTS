import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 7Page_bkspace.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:7Page-bkspace.obj=547e7c15ea446fe3c44a160ebcc1e2c9097d4fb7bea691955255cc16e96ca3c1
    +test_classification:System
    +name: test_pcl5_highvalue_7page_bkspace
    +test:
        +title: test_pcl5_highvalue_7page_bkspace
        +guid:da028bfa-6114-42e9-bf6f-4b28f2ae8a60
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

def test_pcl5_highvalue_7page_bkspace(setup_teardown, printjob, outputsaver):
    printjob.print_verify('547e7c15ea446fe3c44a160ebcc1e2c9097d4fb7bea691955255cc16e96ca3c1')
    outputsaver.save_output()
