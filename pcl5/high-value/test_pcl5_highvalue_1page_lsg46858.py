import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_lsg46858.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-lsg46858.obj=73e01cf4bbb7b3e4ec104dd705efe1e781e411b69c44cada1d60e2675bcfcf02
    +test_classification:System
    +name: test_pcl5_highvalue_1page_lsg46858
    +test:
        +title: test_pcl5_highvalue_1page_lsg46858
        +guid:a4053ef8-2300-4eea-b414-adaad5525099
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

def test_pcl5_highvalue_1page_lsg46858(setup_teardown, printjob, outputsaver):
    printjob.print_verify('73e01cf4bbb7b3e4ec104dd705efe1e781e411b69c44cada1d60e2675bcfcf02', timeout=600)
    outputsaver.save_output()
