import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knhgp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knhgp.obj=14312bb383762b5699ec654a625a18d36e0dfa7fc638bcad968f8939f86c4eca
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knhgp
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knhgp
        +guid:16f4e425-e6b2-4d5e-9f15-90ecef741b03
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knhgp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('14312bb383762b5699ec654a625a18d36e0dfa7fc638bcad968f8939f86c4eca', timeout=600)
    outputsaver.save_output()
