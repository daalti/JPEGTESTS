import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using usb_fpri_8.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:usb_fpri_8.obj=c2b73fd9f28b6fe78084f714743f904fa1ebfad734af40057a67458cdf11af5e
    +test_classification:System
    +name: test_pcl5_pcl_font_feature_usb_fpri_8
    +test:
        +title: test_pcl5_pcl_font_feature_usb_fpri_8
        +guid:389ce769-dd51-4826-9c69-6be72894f42a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_font_feature_usb_fpri_8(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c2b73fd9f28b6fe78084f714743f904fa1ebfad734af40057a67458cdf11af5e', timeout=600)
    outputsaver.save_output()
