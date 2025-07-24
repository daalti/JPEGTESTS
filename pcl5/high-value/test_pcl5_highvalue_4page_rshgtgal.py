import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 4Page_rshgtgal.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:4Page-rshgtgal.obj=381c5a41da3f9a9588d84eba94bc0f3036ba6280341a95e0b451d186c0967d0d
    +test_classification:System
    +name: test_pcl5_highvalue_4page_rshgtgal
    +test:
        +title: test_pcl5_highvalue_4page_rshgtgal
        +guid:5e28b50a-f3c7-41ae-91c3-1794b42b49c7
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

def test_pcl5_highvalue_4page_rshgtgal(setup_teardown, printjob, outputsaver):
    printjob.print_verify('381c5a41da3f9a9588d84eba94bc0f3036ba6280341a95e0b451d186c0967d0d')
    outputsaver.save_output()
