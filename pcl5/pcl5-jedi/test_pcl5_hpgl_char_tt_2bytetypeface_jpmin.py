import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using jpmin.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jpmin.obj=2f6cc3334ed38e06ef800d3438213e1e0ebc8a2525767d7969398b2d68101b0c
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_jpmin
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_jpmin
        +guid:5d1d9897-cba3-450a-aaea-e8a084f00bfb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_jpmin(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2f6cc3334ed38e06ef800d3438213e1e0ebc8a2525767d7969398b2d68101b0c', timeout=600)
    outputsaver.save_output()
