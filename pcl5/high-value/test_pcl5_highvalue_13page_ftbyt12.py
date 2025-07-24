import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 13Page_ftbyt12.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:13Page-ftbyt12.obj=2c252c235aa259ec1e8a3b1366a81f70652c982e5dfe3084d941093600c35128
    +test_classification:System
    +name: test_pcl5_highvalue_13page_ftbyt12
    +test:
        +title: test_pcl5_highvalue_13page_ftbyt12
        +guid:291f050c-76f3-496e-a890-118230af5524
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

def test_pcl5_highvalue_13page_ftbyt12(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2c252c235aa259ec1e8a3b1366a81f70652c982e5dfe3084d941093600c35128', timeout=300)
    outputsaver.save_output()
