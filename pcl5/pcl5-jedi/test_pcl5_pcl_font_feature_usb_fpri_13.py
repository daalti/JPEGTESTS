import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_fpri_13.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:usb_fpri_13.obj=a10cc6bbff29c0e27bcb45ebdc3513a12f939102e0e38b98a4c115c99a86b8ab
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_fpri_13
    +test:
        +title: test_pcl5_pcl_font_feature_usb_fpri_13
        +guid:b6cc10e2-a704-4857-9a91-19add269e603
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_fpri_13(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a10cc6bbff29c0e27bcb45ebdc3513a12f939102e0e38b98a4c115c99a86b8ab', timeout=600)
    outputsaver.save_output()
