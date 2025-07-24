import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 198Page_HebGrkCyrArb.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:198Page-HebGrkCyrArb.obj=2eb974ed3687d0cc633217a6385bf63cbfcd9626084c6abc339b54e6ad85e94e
    +test_classification:System
    +name: test_pcl5_highvalue_198page_hebgrkcyrarb
    +test:
        +title: test_pcl5_highvalue_198page_hebgrkcyrarb
        +guid:fb0c0f4a-5dae-4ab8-9e12-c002b329ce90
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

def test_pcl5_highvalue_198page_hebgrkcyrarb(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2eb974ed3687d0cc633217a6385bf63cbfcd9626084c6abc339b54e6ad85e94e', timeout=3600)
    outputsaver.save_output()
