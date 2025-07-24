import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_logpdefect.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-logpdefect.obj=f5267137f57e5ac763c5d2aca71e2aa2a03f20834c8247e2b1e90446da1b0efe
    +test_classification:System
    +name: test_pcl5_highvalue_1page_logpdefect
    +test:
        +title: test_pcl5_highvalue_1page_logpdefect
        +guid:21ebb3f3-3e0d-414e-b6d7-e64110bdf897
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

def test_pcl5_highvalue_1page_logpdefect(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f5267137f57e5ac763c5d2aca71e2aa2a03f20834c8247e2b1e90446da1b0efe',timeout=600)
    outputsaver.save_output()
