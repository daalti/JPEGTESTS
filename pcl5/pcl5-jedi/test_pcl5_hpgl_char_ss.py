import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ss.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ss.obj=68ae958c9baf7ee0b2771468d256f96e064737752f527fa1fe487575198dca79
    +test_classification:System
    +name: test_pcl5_hpgl_char_ss
    +test:
        +title: test_pcl5_hpgl_char_ss
        +guid:d2711977-a964-421e-b387-e28676ac82cd
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

def test_pcl5_hpgl_char_ss(setup_teardown, printjob, outputsaver):
    printjob.print_verify('68ae958c9baf7ee0b2771468d256f96e064737752f527fa1fe487575198dca79', timeout=600)
    outputsaver.save_output()
