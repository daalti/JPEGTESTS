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
    +external_files:printfile64.urf=e817671f4721a68d82b07970287373822191e33a5699ed3bfb882b7dba475df3
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_DeviceGray_RGB_Duplex_letter_auto_file64
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_DeviceGray_RGB_Duplex_letter_auto_file64
        +guid:86ac80b1-65cb-43f2-aeeb-ebd4a48ed174
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_DeviceGray_RGB_Duplex_letter_auto_file64(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_DeviceGray_RGB_Duplex_letter_auto_file64.test', 'e817671f4721a68d82b07970287373822191e33a5699ed3bfb882b7dba475df3')
    outputsaver.save_output()
