import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knbcf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knbcf.obj=aeac5d8b31c011846a1f05f2e45813cb2640100a484a38852bebf583a7e445a0
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knbcf
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knbcf
        +guid:340c5db3-b82d-4218-a932-1129e3788ded
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

def test_pcl5_hpgl_char_tt_2bytetypeface_knbcf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('aeac5d8b31c011846a1f05f2e45813cb2640100a484a38852bebf583a7e445a0', timeout=600)
    outputsaver.save_output()
