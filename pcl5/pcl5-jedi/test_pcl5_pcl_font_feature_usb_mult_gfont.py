import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_mult_gfont.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:usb_mult_gfont.obj=a17c75617979d2f5eaaf03e88fd56f766cfc81eb5a68c13b908a21602ff3f139
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_mult_gfont
    +test:
        +title: test_pcl5_pcl_font_feature_usb_mult_gfont
        +guid:f019b3ff-55bc-4b25-898f-573c46095437
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_mult_gfont(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a17c75617979d2f5eaaf03e88fd56f766cfc81eb5a68c13b908a21602ff3f139', timeout=600)
    outputsaver.save_output()
