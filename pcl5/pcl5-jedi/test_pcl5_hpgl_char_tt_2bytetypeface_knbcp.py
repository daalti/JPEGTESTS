import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knbcp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knbcp.obj=e8da58c4af6179db794196078d2a8ebe4f2a61f5753eea7581739c5e31ff24a0
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knbcp
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knbcp
        +guid:199d1660-3b32-4f4b-8c40-ac24d4e8057f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knbcp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e8da58c4af6179db794196078d2a8ebe4f2a61f5753eea7581739c5e31ff24a0', timeout=600)
    outputsaver.save_output()
