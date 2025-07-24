import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using fi_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fi_tt.obj=a5943dfde1f19648bfdbd0277df1836fd7316e47d6cf342535fe6c2622a24898
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_fi_tt
    +test:
        +title: test_pcl5_hpgl_char_tt_fi_tt
        +guid:695eca83-f590-48b4-9343-bcd7c2244333
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_fi_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a5943dfde1f19648bfdbd0277df1836fd7316e47d6cf342535fe6c2622a24898', timeout=600)
    outputsaver.save_output()
