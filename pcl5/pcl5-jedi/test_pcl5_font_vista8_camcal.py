import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 font using camcal.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:camcal.obj=cef2c26028e26b7b9cb01cb3176215e36df7475555d6f8ab7ceaeec5b48ebd36
    +test_classification:System
    +name: test_pcl5_font_vista8_camcal
    +test:
        +title: test_pcl5_font_vista8_camcal
        +guid:1c6db253-5535-4669-87e4-20ae8046051a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_font_vista8_camcal(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cef2c26028e26b7b9cb01cb3176215e36df7475555d6f8ab7ceaeec5b48ebd36', timeout=600)
    outputsaver.save_output()
