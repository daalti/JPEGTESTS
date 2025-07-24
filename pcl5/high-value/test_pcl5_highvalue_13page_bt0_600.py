import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 13Page_bt0_600.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:13Page-bt0_600.obj=5dad4f1c3642b067f61505ff5e93ca2237298849996e91205a0e7d1fac5263f9
    +test_classification:System
    +name: test_pcl5_highvalue_13page_bt0_600
    +test:
        +title: test_pcl5_highvalue_13page_bt0_600
        +guid:906c3d95-2063-4d11-8569-23220939fe1d
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

def test_pcl5_highvalue_13page_bt0_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5dad4f1c3642b067f61505ff5e93ca2237298849996e91205a0e7d1fac5263f9', timeout=300)
    outputsaver.save_output()
