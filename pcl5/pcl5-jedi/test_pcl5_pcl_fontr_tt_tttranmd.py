import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tttranmd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tttranmd.obj=4e8c22602b6953d539750cf54c39062726485c4f017d58958d9d34c77630caa8
    +test_classification:System
    +name: test_pcl5_pcl_fontr_tt_tttranmd
    +test:
        +title: test_pcl5_pcl_fontr_tt_tttranmd
        +guid:642d6dd4-715a-4e00-bb41-63a106fb61d9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontr_tt_tttranmd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4e8c22602b6953d539750cf54c39062726485c4f017d58958d9d34c77630caa8', timeout=600)
    outputsaver.save_output()
