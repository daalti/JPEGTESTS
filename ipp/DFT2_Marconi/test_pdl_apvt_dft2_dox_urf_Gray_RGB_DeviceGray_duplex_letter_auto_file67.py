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
    +external_files:printfile67.urf=451b3191df6f4059f565cce1d404d0a4aeff38bc5c5354c90c5630c5c9d6501d
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_Gray_RGB_DeviceGray_duplex_letter_auto_file67
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_Gray_RGB_DeviceGray_duplex_letter_auto_file67
        +guid:726e498b-7058-4044-93e6-68e6ad6e2ef4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_Gray_RGB_DeviceGray_duplex_letter_auto_file67(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_Gray_RGB_DeviceGray_duplex_letter_auto_file67.test', '451b3191df6f4059f565cce1d404d0a4aeff38bc5c5354c90c5630c5c9d6501d')
    outputsaver.save_output()
