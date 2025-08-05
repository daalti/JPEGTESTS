import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile58.urf=8cfa74ec3c6e03bb27be6d2f0805e71d5c948770d4d634d8a7479e13d88500c9
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_duplex_device_RGB_normal_letter_auto_file59
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_duplex_device_RGB_normal_letter_auto_file59
        +guid:b9b025d6-5dc4-44ed-9da7-e0d5559622b9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_duplex_device_RGB_normal_letter_auto_file59(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_duplex_device_RGB_normal_letter_auto_file59.test', '8cfa74ec3c6e03bb27be6d2f0805e71d5c948770d4d634d8a7479e13d88500c9')
    outputsaver.save_output()
