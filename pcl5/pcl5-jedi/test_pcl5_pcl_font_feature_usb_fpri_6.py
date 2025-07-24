import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_fpri_6.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:usb_fpri_6.obj=f79ee31f938564e79e4cadc702ab93ddeeb5ba53492788129b73b2f18ab8572a
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_fpri_6
    +test:
        +title: test_pcl5_pcl_font_feature_usb_fpri_6
        +guid:2e0001ba-2c9e-4bd0-a215-51a99e01937b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_fpri_6(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f79ee31f938564e79e4cadc702ab93ddeeb5ba53492788129b73b2f18ab8572a', timeout=600)
    outputsaver.save_output()
