import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_fpri_8_hw.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:usb_fpri_8_hw.obj=a3d6425ec44e0c3800d80e3b2a443cee94bb003e197c39885e7a7423d985aa01
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_fpri_8_hw
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_font_feature_usb_fpri_8_hw
        +guid:e0269f94-d22c-4560-8c34-6bfbf5f7753b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_fpri_8_hw(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a3d6425ec44e0c3800d80e3b2a443cee94bb003e197c39885e7a7423d985aa01', timeout=600)
    outputsaver.save_output()
