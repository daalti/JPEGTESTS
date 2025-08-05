import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile8.jpg=951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_jpeg_600dpi_RGB_normal_letter_auto_fit_file23
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_jpeg_600dpi_RGB_normal_letter_auto_fit_file23
        +guid:6827ff78-5856-43f4-aff1-905b41c3f90f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_jpeg_600dpi_RGB_normal_letter_auto_fit_file23(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_jpeg_600dpi_RGB_normal_letter_auto_fit_file23.test', '951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4')
    outputsaver.save_output()
