import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_fpri_12.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:usb_fpri_12.obj=2cb44358c592547b761d0956b495b0c6d5eec481c6baea4ffa1c24d875d0ca6e
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_fpri_12
    +test:
        +title: test_pcl5_pcl_font_feature_usb_fpri_12
        +guid:1ebdf4fb-d226-47ba-b8cc-d3da156d15b3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_fpri_12(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2cb44358c592547b761d0956b495b0c6d5eec481c6baea4ffa1c24d875d0ca6e', timeout=600)
    outputsaver.save_output()
