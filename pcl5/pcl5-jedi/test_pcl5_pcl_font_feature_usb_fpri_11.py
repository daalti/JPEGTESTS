import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_fpri_11.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:usb_fpri_11.obj=8e30d0ef2f9adc94338ed403a2d42ebb8c3ab8ba0a5e9d0bce8d12e40059744b
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_fpri_11
    +test:
        +title: test_pcl5_pcl_font_feature_usb_fpri_11
        +guid:8971b5ca-0902-4580-9fb9-85867de09c2f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_fpri_11(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8e30d0ef2f9adc94338ed403a2d42ebb8c3ab8ba0a5e9d0bce8d12e40059744b', timeout=600)
    outputsaver.save_output()
