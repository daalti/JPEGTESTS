import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using jppminv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jppminv.obj=e6a0ce94f5a0a1b017b411ed93e13f598c76e6c66cad16ebca1a9cba365684fc
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_jppminv
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_jppminv
        +guid:47f60498-d221-442b-82ad-aa6d3392158d
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

def test_pcl5_hpgl_char_tt_2bytetypeface_jppminv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('e6a0ce94f5a0a1b017b411ed93e13f598c76e6c66cad16ebca1a9cba365684fc', timeout=600)
    outputsaver.save_output()
