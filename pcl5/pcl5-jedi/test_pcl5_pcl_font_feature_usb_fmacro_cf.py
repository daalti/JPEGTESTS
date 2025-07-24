import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_fmacro_cf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:usb_fmacro_cf.obj=2bec6274ea7becdf534a323576bb64b9946e5525214e13dd1759ebb6e2172dfe
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_fmacro_cf
    +test:
        +title: test_pcl5_pcl_font_feature_usb_fmacro_cf
        +guid:5f36efcc-f58a-416d-9b2e-a3f60aefc0f7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_fmacro_cf(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('2bec6274ea7becdf534a323576bb64b9946e5525214e13dd1759ebb6e2172dfe', timeout=600,expected_jobs=2)
    outputsaver.save_output()
