import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ss_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ss_tt.obj=a99c394a9335dd61c6401a1eeb75f94893e13f1cc127b1c47276e04b720e26fb
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_ss_tt
    +test:
        +title: test_pcl5_hpgl_char_tt_ss_tt
        +guid:e83f5f3e-8bfd-47a4-be2f-1723caf4608d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_ss_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a99c394a9335dd61c6401a1eeb75f94893e13f1cc127b1c47276e04b720e26fb', timeout=600)
    outputsaver.save_output()
