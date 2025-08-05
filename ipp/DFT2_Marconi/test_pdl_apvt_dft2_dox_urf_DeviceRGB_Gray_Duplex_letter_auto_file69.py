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
    +external_files:printfile69.urf=67cf4b6d971c520749ac56f3e1d1d990f5fe096837c29c5d3a96bf6851a8a04c
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_DeviceRGB_Gray_Duplex_letter_auto_file69
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_DeviceRGB_Gray_Duplex_letter_auto_file69
        +guid:97cb41d3-df39-4b02-8903-a035a295cde6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_DeviceRGB_Gray_Duplex_letter_auto_file69(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_DeviceRGB_Gray_Duplex_letter_auto_file69.test', '67cf4b6d971c520749ac56f3e1d1d990f5fe096837c29c5d3a96bf6851a8a04c')
    outputsaver.save_output()
