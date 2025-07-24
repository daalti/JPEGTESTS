import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 4Page_siso.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:4Page-siso.obj=70b8433ef21a1bf8c721170a447b07141b3007f4d36490ab40b41437f266433e
    +test_classification:System
    +name: test_pcl5_highvalue_4page_siso
    +test:
        +title: test_pcl5_highvalue_4page_siso
        +guid:ccdba16c-e889-4714-a574-7c7713973b01
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

def test_pcl5_highvalue_4page_siso(setup_teardown, printjob, outputsaver):
    printjob.print_verify('70b8433ef21a1bf8c721170a447b07141b3007f4d36490ab40b41437f266433e')
    outputsaver.save_output()
