import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using td_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:td_tt.obj=861faef8ebfda970a242f29d4c1224b1cc20c15d4e85cd99a4d70ec80f04e679
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_td_tt
    +test:
        +title: test_pcl5_hpgl_char_tt_td_tt
        +guid:50cecdac-ca8d-443b-a668-186180d622c6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_td_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('861faef8ebfda970a242f29d4c1224b1cc20c15d4e85cd99a4d70ec80f04e679', timeout=600)
    outputsaver.save_output()
