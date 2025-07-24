import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_gpri_1.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:usb_gpri_1.obj=a8310d818f3112bdd9fc2c1d1bd837c9ce5308a372add182643dad35f3bd470b
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_gpri_1
    +test:
        +title: test_pcl5_pcl_font_feature_usb_gpri_1
        +guid:7f6b74da-60ce-4edf-8047-cecf5e7d301e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_gpri_1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a8310d818f3112bdd9fc2c1d1bd837c9ce5308a372add182643dad35f3bd470b', timeout=600)
    outputsaver.save_output()
