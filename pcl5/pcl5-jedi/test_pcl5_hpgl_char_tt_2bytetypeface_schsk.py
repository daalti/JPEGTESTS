import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using schsk.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:schsk.obj=dd16356c6887e4a80d8fd9178d08fb1e86efb8fa05fb9a11d031af8ac6d1c2fa
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_schsk
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_schsk
        +guid:6edb8010-0fd3-4ec7-9ef1-955a7543e551
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_schsk(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dd16356c6887e4a80d8fd9178d08fb1e86efb8fa05fb9a11d031af8ac6d1c2fa', timeout=600)
    outputsaver.save_output()
