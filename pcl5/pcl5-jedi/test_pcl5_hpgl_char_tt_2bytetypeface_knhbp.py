import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knhbp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knhbp.obj=8b2a3d95e8279e9ec13675147616069e6856fdd5c1483042725d708facad9c5b
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knhbp
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knhbp
        +guid:316ed60f-e417-4e00-b55a-b89e0dff71c9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knhbp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8b2a3d95e8279e9ec13675147616069e6856fdd5c1483042725d708facad9c5b', timeout=600)
    outputsaver.save_output()
