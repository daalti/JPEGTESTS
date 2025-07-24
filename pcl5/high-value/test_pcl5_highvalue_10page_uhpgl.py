import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 10Page_uhpgl.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:10Page-uhpgl.obj=dd892ecb18733e631c668b08ced3b950d2dc79697729f31cb41c1f61523bd219
    +test_classification:System
    +name: test_pcl5_highvalue_10page_uhpgl
    +test:
        +title: test_pcl5_highvalue_10page_uhpgl
        +guid:f44a79a0-cdde-41df-b78d-0292646ca192
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

def test_pcl5_highvalue_10page_uhpgl(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dd892ecb18733e631c668b08ced3b950d2dc79697729f31cb41c1f61523bd219', timeout=300)
    outputsaver.save_output()
