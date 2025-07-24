import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_fpri_9.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:usb_fpri_9.obj=71a25c4db74bcb0e8bc79c9bf4d119c47c72ed99f7e3695f57c3e3af2e1ed34d
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_fpri_9
    +test:
        +title: test_pcl5_pcl_font_feature_usb_fpri_9
        +guid:8d2e3367-90e5-4aac-a555-bbf4dd1d4657
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_fpri_9(setup_teardown, printjob, outputsaver):
    printjob.print_verify('71a25c4db74bcb0e8bc79c9bf4d119c47c72ed99f7e3695f57c3e3af2e1ed34d', timeout=600)
    outputsaver.save_output()
