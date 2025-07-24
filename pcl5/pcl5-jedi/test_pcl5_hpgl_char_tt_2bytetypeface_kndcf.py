import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using kndcf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kndcf.obj=4b4e0fb96a5c17de7c14a9031f17efed74ab7ceebafef0975f57fc61d2e855b6
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_kndcf
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_kndcf
        +guid:8e08353c-0858-4db9-8750-5c89a48c52d5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_kndcf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4b4e0fb96a5c17de7c14a9031f17efed74ab7ceebafef0975f57fc61d2e855b6', timeout=600)
    outputsaver.save_output()
