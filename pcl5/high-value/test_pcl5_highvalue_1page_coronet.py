import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_coronet.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-coronet.obj=1287cd384473b286b93f36dc1209c470041f31a1d0099d989a027fece696f875
    +test_classification:System
    +name: test_pcl5_highvalue_1page_coronet
    +test:
        +title: test_pcl5_highvalue_1page_coronet
        +guid:7460ad23-5e3e-449f-b5c5-fa907b72047c
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

def test_pcl5_highvalue_1page_coronet(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1287cd384473b286b93f36dc1209c470041f31a1d0099d989a027fece696f875')
    outputsaver.save_output()
