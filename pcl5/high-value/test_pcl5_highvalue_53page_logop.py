import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 53Page_logop.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1500
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:53Page-logop.obj=72cac21cf1973e4374465df894209054ffee1787ed34fc25786e738e02bd22d1
    +test_classification:System
    +name: test_pcl5_highvalue_53page_logop
    +test:
        +title: test_pcl5_highvalue_53page_logop
        +guid:e39eb396-7350-43cd-9e3e-373eadb589af
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

def test_pcl5_highvalue_53page_logop(setup_teardown, printjob, outputsaver):
    printjob.print_verify('72cac21cf1973e4374465df894209054ffee1787ed34fc25786e738e02bd22d1', timeout=1500)
    outputsaver.save_output()
